import numpy as np
import polars as pl
from datetime import datetime
from data.calculate_dl import calculate_dl
from data.dl import dl_base
from bussiness.craw_data_bl import resample_ohlcv

INDICATOR_INDEXES = [[("Ticker", 1), ("DateTime", 1)]]
ALERT_INDEXES = [[("Ticker", 1), ("DateTime", 1), ("timeframe", 1)], [("type", 1)]]
NOTE_2_BOTTOM = "MACD phân kỳ 2 đáy"
NOTE_2_TOP = "MACD phân kỳ 2 đỉnh"


def calculate_update_technical_analysis():
    daily = pl.DataFrame(dl_base.get_docs("stock"))
    if daily.is_empty():
        return "No stock data"

    daily = _normalize_ohlcv(daily)
    weekly = resample_ohlcv(daily, "1w")
    monthly = resample_ohlcv(daily, "1mo")
    dl_base.replace_dataframe("stock_week", weekly, INDICATOR_INDEXES)
    dl_base.replace_dataframe("stock_month", monthly, INDICATOR_INDEXES)

    frames = []
    alerts = []
    for timeframe, source, left, right in (
        ("daily", daily, 5, 5),
        ("weekly", weekly, 3, 3),
        ("monthly", monthly, 2, 2),
    ):
        indicators, tf_alerts = _build_indicators(source, timeframe, left, right)
        frames.append((timeframe, indicators))
        alerts.extend(tf_alerts)

    collection_map = {
        "daily": "indicators",
        "weekly": "indicators_week",
        "monthly": "indicators_month",
    }
    for timeframe, indicators in frames:
        dl_base.replace_dataframe(
            collection_map[timeframe],
            indicators,
            INDICATOR_INDEXES,
        )
    dl_base.replace_collection("macd_alerts", alerts, ALERT_INDEXES)
    return "Success"


def _normalize_ohlcv(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.select(["Ticker", "DateTime", "Open", "High", "Low", "Close", "Volume"])
        .with_columns(
            pl.col("Ticker").cast(pl.Utf8),
            pl.col("DateTime").cast(pl.Int64),
            pl.col("Open").cast(pl.Float64),
            pl.col("High").cast(pl.Float64),
            pl.col("Low").cast(pl.Float64),
            pl.col("Close").cast(pl.Float64),
            pl.col("Volume").cast(pl.Float64),
        )
        .drop_nulls(["Ticker", "DateTime", "Close"])
        .unique(subset=["Ticker", "DateTime"], keep="last")
        .sort(["Ticker", "DateTime"])
    )


def _build_indicators(ohlcv: pl.DataFrame, timeframe: str, left: int, right: int):
    df = _add_ma_macd(ohlcv)
    parts = []
    alerts = []
    for group in df.partition_by("Ticker", maintain_order=True):
        marked, group_alerts = _mark_macd_divergence(group, timeframe, left, right)
        parts.append(marked)
        alerts.extend(group_alerts)
    if not parts:
        return df, alerts
    return pl.concat(parts, how="vertical"), alerts


def _add_ma_macd(df: pl.DataFrame) -> pl.DataFrame:
    close = pl.col("Close")
    return (
        df.sort(["Ticker", "DateTime"])
        .with_columns(
            close.rolling_mean(window_size=20).over("Ticker").alias("MA20"),
            close.rolling_mean(window_size=50).over("Ticker").alias("MA50"),
            close.rolling_mean(window_size=100).over("Ticker").alias("MA100"),
            close.ewm_mean(span=12, adjust=False).over("Ticker").alias("_ema12"),
            close.ewm_mean(span=26, adjust=False).over("Ticker").alias("_ema26"),
        )
        .with_columns((pl.col("_ema12") - pl.col("_ema26")).alias("macd"))
        .with_columns(
            pl.col("macd")
            .ewm_mean(span=9, adjust=False)
            .over("Ticker")
            .alias("macdsignal")
        )
        .with_columns((pl.col("macd") - pl.col("macdsignal")).alias("macdhist"))
        .drop(["_ema12", "_ema26"])
    )


def _mark_macd_divergence(df: pl.DataFrame, timeframe: str, left: int, right: int):
    n = df.height
    bottom_flag = np.zeros(n, dtype=np.int8)
    top_flag = np.zeros(n, dtype=np.int8)
    notes = np.array([None] * n, dtype=object)
    alerts = []
    if n < left + right + 3:
        return (
            df.with_columns(
                pl.Series("macd_div_2_bottom", bottom_flag),
                pl.Series("macd_div_2_top", top_flag),
                pl.Series("macd_div_note", list(notes), dtype=pl.Utf8),
            ),
            alerts,
        )

    close = df["Close"].to_numpy()
    low = df["Low"].to_numpy() if "Low" in df.columns else close
    high = df["High"].to_numpy() if "High" in df.columns else close
    macd = df["macd"].to_numpy()
    dates = df["DateTime"].to_numpy()
    ticker = df["Ticker"][0]

    swing_lows = _swing_points(low, left, right, find_max=False)
    swing_highs = _swing_points(high, left, right, find_max=True)

    for first, second in zip(swing_lows[:-1], swing_lows[1:]):
        if np.isnan(macd[first]) or np.isnan(macd[second]):
            continue
        if (
            low[second] < low[first]
            and macd[second] > macd[first]
            and macd[first] < 0
            and macd[second] < 0
        ):
            confirm = min(second + right, n - 1)
            bottom_flag[confirm] = 1
            notes[confirm] = _join_note(notes[confirm], NOTE_2_BOTTOM)
            alerts.append(
                _alert_doc(
                    ticker,
                    timeframe,
                    dates[confirm],
                    "macd_div_2_bottom",
                    NOTE_2_BOTTOM,
                    dates[first],
                    dates[second],
                    low[first],
                    low[second],
                    macd[first],
                    macd[second],
                )
            )

    for first, second in zip(swing_highs[:-1], swing_highs[1:]):
        if np.isnan(macd[first]) or np.isnan(macd[second]):
            continue
        if (
            high[second] > high[first]
            and macd[second] < macd[first]
            and macd[first] > 0
            and macd[second] > 0
        ):
            confirm = min(second + right, n - 1)
            top_flag[confirm] = 1
            notes[confirm] = _join_note(notes[confirm], NOTE_2_TOP)
            alerts.append(
                _alert_doc(
                    ticker,
                    timeframe,
                    dates[confirm],
                    "macd_div_2_top",
                    NOTE_2_TOP,
                    dates[first],
                    dates[second],
                    high[first],
                    high[second],
                    macd[first],
                    macd[second],
                )
            )

    return (
        df.with_columns(
            pl.Series("macd_div_2_bottom", bottom_flag),
            pl.Series("macd_div_2_top", top_flag),
            pl.Series("macd_div_note", list(notes), dtype=pl.Utf8),
        ),
        alerts,
    )


def _swing_points(values, left, right, find_max: bool):
    points = []
    n = len(values)
    for i in range(left, n - right):
        window = values[i - left : i + right + 1]
        if np.isnan(values[i]) or np.isnan(window).any():
            continue
        if find_max:
            if values[i] == np.nanmax(window) and int(np.nanargmax(window)) == left:
                points.append(i)
        else:
            if values[i] == np.nanmin(window) and int(np.nanargmin(window)) == left:
                points.append(i)
    return points


def _join_note(current, note):
    if current is None:
        return note
    if note in str(current):
        return current
    return f"{current}; {note}"


def _alert_doc(
    ticker,
    timeframe,
    datetime_value,
    alert_type,
    note,
    date_1,
    date_2,
    price_1,
    price_2,
    macd_1,
    macd_2,
):
    return {
        "Ticker": ticker,
        "timeframe": timeframe,
        "DateTime": int(datetime_value),
        "type": alert_type,
        "note": note,
        "date_1": int(date_1),
        "date_2": int(date_2),
        "price_1": float(price_1),
        "price_2": float(price_2),
        "macd_1": float(macd_1),
        "macd_2": float(macd_2),
    }


def caculate_macd_signal_buy(date_before=3):
    if date_before > 100:
        date_before = 100
    current_Date = datetime.now()
    current_date_number = (
        current_Date.year * 10000 + current_Date.month * 100 + current_Date.day
    )
    date_query = current_date_number - date_before - 2
    list_data = calculate_dl.get_data(
        "indicators",
        {"DateTime": {"$gte": date_query}},
        [["Ticker", 1], ("DateTime", 1)],
    )
    df = pl.DataFrame(list_data)
    macd_buy, macd_sell = macd_signal(df)
    new_df = df.select(
        pl.col("Ticker"),
        pl.col("DateTime"),
        pl.Series("macd_buy", macd_buy, dtype=pl.Float32),
        pl.Series("macd_sell", macd_sell, dtype=pl.Float32),
    ).filter(pl.col("macd_buy") != -1)
    return new_df.to_dicts()


def macd_signal(df):
    macd_buy = []
    macd_sell = []
    position = False
    current_ticker = ""
    new_ticker = True
    for i in range(0, len(df)):
        if current_ticker != df["Ticker"][i]:
            new_ticker = True
            current_ticker = df["Ticker"][i]
        else:
            new_ticker = False
        if i == 0 or new_ticker:
            macd_buy.append(-1)
            macd_sell.append(-1)
        else:
            if df["macdhist"][i] > 0 and df["macdhist"][i - 1] <= 0:
                macd_sell.append(-1)
                if position == False:
                    macd_buy.append(df["Close"][i])
                    position = True
                else:
                    macd_buy.append(-1)
            elif df["macdhist"][i] < 0 and df["macdhist"][i - 1] >= 0:
                macd_buy.append(-1)
                if position == True:
                    macd_sell.append(df["Close"][i])
                    position = False
                else:
                    macd_sell.append(-1)
            else:
                macd_buy.append(-1)
                macd_sell.append(-1)
    return macd_buy, macd_sell
