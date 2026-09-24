from datetime import datetime, timedelta
from zipfile import ZipFile
import os
import glob
import polars as pl
from data.dl import dl_base
from utils import call_api

STOCK_INDEXES = [[("Ticker", 1), ("DateTime", 1)]]
MARKET_FILES = ("HNX", "HSX", "UPCOM")


def craw_data(current_date, max_retry=10):
    last_error = None
    for offset in range(max_retry):
        day = current_date - timedelta(days=offset)
        try:
            if _import_day(day):
                return "Success"
        except Exception as e:
            last_error = e
            print(e)
            _cleanup_cafef_files()
    if last_error:
        raise last_error
    return "Failed"


def _import_day(day: datetime) -> bool:
    day_format = day.strftime("%d%m%Y")
    day_number = day.strftime("%Y%m%d")
    day_point = day.strftime("%d.%m.%Y")
    stock_url = f"https://cafef1.mediacdn.vn/data/ami_data/{day_number}/CafeF.SolieuGD.Upto{day_format}.zip"
    index_url = f"https://cafef1.mediacdn.vn/data/ami_data/{day_number}/CafeF.Index.Upto{day_format}.zip"
    print(stock_url)
    call_api.call_download(stock_url, "data.zip")
    _unzip_data("data.zip")
    daily = _read_market_csvs(day_point)
    if daily.is_empty():
        raise ValueError("No market CSV data")
    index_df = _download_index(index_url, day_point)
    if index_df is not None and not index_df.is_empty():
        daily = pl.concat([daily, index_df], how="vertical")
    daily = daily.with_columns(pl.col("Ticker").str.to_uppercase())
    daily = daily.unique(subset=["Ticker", "DateTime"], keep="last").sort(
        ["Ticker", "DateTime"]
    )
    weekly = resample_ohlcv(daily, "1w")
    monthly = resample_ohlcv(daily, "1mo")
    dl_base.replace_dataframe("stock", daily, STOCK_INDEXES)
    dl_base.replace_dataframe("stock_week", weekly, STOCK_INDEXES)
    dl_base.replace_dataframe("stock_month", monthly, STOCK_INDEXES)
    _cleanup_cafef_files()
    return True


def _download_index(index_url: str, day_point: str) -> pl.DataFrame | None:
    print(index_url)
    try:
        call_api.call_download(index_url, "index.zip")
        _unzip_data("index.zip")
        return _read_index_csv(day_point)
    except Exception as e:
        print("Skip CafeF index (VNINDEX):", e)
        return None


def _read_index_csv(day_point: str) -> pl.DataFrame:
    path = f"CafeF.INDEX.Upto{day_point}.csv"
    if not os.path.exists(path):
        matches = glob.glob("CafeF.INDEX*.csv") + glob.glob("CafeF.Index*.csv")
        if not matches:
            return _empty_ohlcv()
        path = matches[0]
    df = _read_cafef_csv(path).with_columns(pl.col("Ticker").str.to_uppercase())
    return df.filter(pl.col("Ticker").is_in(["VNINDEX", "HNX-INDEX", "VN30"]))


def resample_ohlcv(daily: pl.DataFrame, every: str) -> pl.DataFrame:
    work = daily.with_columns(
        pl.col("DateTime").cast(pl.Utf8).str.to_date("%Y%m%d").alias("_date")
    ).sort(["Ticker", "_date"])
    period = pl.col("_date").dt.truncate(every)
    return (
        work.with_columns(period.alias("_period"))
        .group_by(["Ticker", "_period"])
        .agg(
            pl.col("DateTime").sort_by("_date").last(),
            pl.col("Open").sort_by("_date").first(),
            pl.col("High").max(),
            pl.col("Low").min(),
            pl.col("Close").sort_by("_date").last(),
            pl.col("Volume").sum(),
        )
        .drop("_period")
        .sort(["Ticker", "DateTime"])
    )


def _unzip_data(zip_name: str):
    with ZipFile(zip_name, "r") as z_object:
        z_object.extractall()
    if os.path.exists(zip_name):
        os.remove(zip_name)


def _read_market_csvs(day_point: str) -> pl.DataFrame:
    frames = []
    for market in MARKET_FILES:
        path = f"CafeF.{market}.Upto{day_point}.csv"
        if not os.path.exists(path):
            continue
        frames.append(_read_cafef_csv(path))
    if not frames:
        return _empty_ohlcv()
    return pl.concat(frames, how="vertical")


def _empty_ohlcv() -> pl.DataFrame:
    return pl.DataFrame(
        schema={
            "Ticker": pl.Utf8,
            "DateTime": pl.Int64,
            "Open": pl.Float64,
            "High": pl.Float64,
            "Low": pl.Float64,
            "Close": pl.Float64,
            "Volume": pl.Float64,
        }
    )


def _read_cafef_csv(path: str) -> pl.DataFrame:
    df = pl.read_csv(path, infer_schema_length=2000, ignore_errors=True)
    rename = {col: col.replace("<", "").replace(">", "").strip() for col in df.columns}
    df = df.rename(rename)
    mapping = {}
    for col in df.columns:
        key = col.strip().upper()
        if key in {"TICKER", "CODE", "SYMBOL"}:
            mapping[col] = "Ticker"
        elif key in {"DTYYYYMMDD", "DATETIME", "DATE"}:
            mapping[col] = "DateTime"
        elif key == "OPEN":
            mapping[col] = "Open"
        elif key == "HIGH":
            mapping[col] = "High"
        elif key == "LOW":
            mapping[col] = "Low"
        elif key == "CLOSE":
            mapping[col] = "Close"
        elif key in {"VOLUME", "VOL"}:
            mapping[col] = "Volume"
    df = df.rename(mapping)
    df = df.select(["Ticker", "DateTime", "Open", "High", "Low", "Close", "Volume"])
    return df.with_columns(
        pl.col("Ticker").cast(pl.Utf8).str.replace_all(r"[<>]", ""),
        pl.col("DateTime").cast(pl.Utf8).str.replace_all(r"[<>]", "").cast(pl.Int64),
        pl.col("Open").cast(pl.Float64),
        pl.col("High").cast(pl.Float64),
        pl.col("Low").cast(pl.Float64),
        pl.col("Close").cast(pl.Float64),
        pl.col("Volume").cast(pl.Float64),
    )


def _cleanup_cafef_files():
    for path in (
        glob.glob("CafeF*.csv") + glob.glob("data.zip") + glob.glob("index.zip")
    ):
        try:
            os.remove(path)
        except OSError:
            pass
