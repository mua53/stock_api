import dl
import os
import call_api

def insert_stock():
    return None

def get_info_indicator_stock(stock_code):
    url = os.getenv('URL_VIETSTOCK') + 'company/tradinginfo'
    payload = "code=" + stock_code + "&s=0&t=&__RequestVerificationToken=JX9xDCZlmnaLjb11sB19jYFaj_3W5UJEyvSzb_yDcotKvsI4BV4GPc5OE1N7ZHg_D_XIow9zXf1gYDoMIyQtSl7_3oHH_AbWN8XG8KzsOJI1"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'finance.vietstock.vn',
        'Origin': 'https://finance.vietstock.vn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://finance.vietstock.vn/chi-so-nganh.htm',
        'Content-Length': '142',
        'Cookie': '_ga_EXMM0DKVEX=GS1.1.1678756915.9.1.1678756962.0.0.0; language=vi-VN; cto_bidid=bWJVU19lZjlKSEZTUHJaayUyRnlKRXBoSFlZdXRkZGxRb1FndHdtRzlZVDJEejlpYXdnY1VEZVQ3QzdYajBMdTdGTWt0QVVLUVVOS1pOQkZTMm85UyUyRjJWS01IOUElM0QlM0Q; cto_bundle=Csd0zV94YmklMkYybFJhTFF1dHAzcGZ1THlPR05RSW8zUmwzUVBIeHJVWkJTdXhjNEdwZTAlMkJRdkp3SUUlMkZUSWFmMVp5dzBPS2dGNkplckRCNFolMkZWQkQ3T3FqbCUyRm5TcVBHVnMlMkJCbTZ5Zk03ODNrVW9yS0d4WE0xenppSUZSbEVJQUxqNmRzZw; _ga=GA1.1.978692422.1678338963; _pbjs_userid_consent_data=3524755945110770; _cc_id=759c398130928dfbb4ed80efa1b1ec7; panoramaId_expiry=1678843317938; __gads=ID=1be65e2576ea1501-220a6471bade0083:T=1678338964:RT=1678756915:S=ALNI_MZW8ixDEwymAY3_YRi9tMSMvYgkpA; ASP.NET_SessionId=qybmwwurpbliursgjjwazy3z; __RequestVerificationToken=QzOlAVTJVvLk3S1adbkdFcX5O5BotHf6zgSPf4rMErB5icREOl-ISQyLQS-sH_eAjjlSLIZ2FuMrp5NVeiJO0a9EcNVLSZf2yBgoaVpDVnU1; __gpi=UID=000009d68283f1cf:T=1678338964:RT=1678756915:S=ALNI_MYpVyVGiNNzWZ_cT-mjhDYhIHpNrQ; isShowLogin=true; AnonymousNotification=; Theme=Light; dable_uid=29430766.1678338990858',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = call_api.call_post(url, headers,payload)
    return response

def get_info_finance_stock(stock_code):
    return None

def get_info_branch():
    return None

def insert_info_career():
    data = get_info_career()
    for item in data:
        item['']
    dl.insert_data('career',data)
    
def get_info_career():
    url = os.getenv('URL_VIETSTOCK') + "data/sectionindex"
    payload = "type=1&__RequestVerificationToken=QnJ1Dm_vZRFQ3JP9nsKxo5xxSZPMZSOfI-5Gd8B4HrPMReoUe7sp-h78lxGz5hZoWkcnR9NZXjRCRHvy-kmzPJxLGPn1TZdQ1g01aV_BSUA1"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'finance.vietstock.vn',
        'Origin': 'https://finance.vietstock.vn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://finance.vietstock.vn/chi-so-nganh.htm',
        'Content-Length': '142',
        'Cookie': '_ga_EXMM0DKVEX=GS1.1.1678756915.9.1.1678756962.0.0.0; language=vi-VN; cto_bidid=bWJVU19lZjlKSEZTUHJaayUyRnlKRXBoSFlZdXRkZGxRb1FndHdtRzlZVDJEejlpYXdnY1VEZVQ3QzdYajBMdTdGTWt0QVVLUVVOS1pOQkZTMm85UyUyRjJWS01IOUElM0QlM0Q; cto_bundle=Csd0zV94YmklMkYybFJhTFF1dHAzcGZ1THlPR05RSW8zUmwzUVBIeHJVWkJTdXhjNEdwZTAlMkJRdkp3SUUlMkZUSWFmMVp5dzBPS2dGNkplckRCNFolMkZWQkQ3T3FqbCUyRm5TcVBHVnMlMkJCbTZ5Zk03ODNrVW9yS0d4WE0xenppSUZSbEVJQUxqNmRzZw; _ga=GA1.1.978692422.1678338963; _pbjs_userid_consent_data=3524755945110770; _cc_id=759c398130928dfbb4ed80efa1b1ec7; panoramaId_expiry=1678843317938; __gads=ID=1be65e2576ea1501-220a6471bade0083:T=1678338964:RT=1678756915:S=ALNI_MZW8ixDEwymAY3_YRi9tMSMvYgkpA; ASP.NET_SessionId=qybmwwurpbliursgjjwazy3z; __RequestVerificationToken=QzOlAVTJVvLk3S1adbkdFcX5O5BotHf6zgSPf4rMErB5icREOl-ISQyLQS-sH_eAjjlSLIZ2FuMrp5NVeiJO0a9EcNVLSZf2yBgoaVpDVnU1; __gpi=UID=000009d68283f1cf:T=1678338964:RT=1678756915:S=ALNI_MYpVyVGiNNzWZ_cT-mjhDYhIHpNrQ; isShowLogin=true; AnonymousNotification=; Theme=Light; dable_uid=29430766.1678338990858',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = call_api.call_post(url, headers, payload)
    return response

def draw_index_career():
    return None

