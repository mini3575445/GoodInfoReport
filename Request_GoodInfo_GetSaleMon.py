import requests
from bs4 import BeautifulSoup

#請求這個網址，回傳html
url = 'https://goodinfo.tw/tw/ShowSaleMonChart.asp?STEP=DATA&STOCK_ID=2357&PRICE_ADJ=F&START_DT=2021-03-20&END_DT=2024-07-19'

headers = {
    'accept': '*/*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '0',
    'content-type': 'application/x-www-form-urlencoded;',
    'cookie': '_ga=GA1.1.703480984.1681461182; CLIENT%5FID=20240705161355539%5F210%2E61%2E205%2E217; LOGIN=EMAIL=mini3575445%40gmail%2Ecom&USER%5FNM=%E6%9F%AF%E6%98%B1%E5%BB%B7&ACCOUNT%5FID=108479803592423432175&ACCOUNT%5FVENDOR=Google&NO%5FEXPIRE=T; IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=1920&HEIGHT=1080; TW_STOCK_BROWSE_LIST=2357%7C2454%7C2330%7C2370%7C3711%7C3533%7C6180; _ga_0LP5MLQS7E=GS1.1.1721373857.16.1.1721374124.55.0.0',
    'origin': 'https://goodinfo.tw',
    'priority': 'u=1, i',
    'referer': 'https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID=2357',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

response = requests.post(url, headers=headers)

# 檢查請求是否成功
if response.status_code == 200:
    data = response.text
    print(data)
else:
    print(f"請求失敗，狀態碼: {response.status_code}")