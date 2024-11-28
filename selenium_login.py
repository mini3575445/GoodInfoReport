import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import jwt
import datetime
_dicStock = {}  #字典放class Stock
def Get_stock_field_values(stock_dict, field_name) -> list: 
    """
    從字典中取得所有股票物件中特定欄位的值。

    :param stock_dict: 包含股票物件的字典。
    :param field_name: 要取得的欄位名稱。
    :return: 包含特定欄位值的列表。
    """
    field_values = []
    for stock in stock_dict.values():
        field_values.append(getattr(stock, field_name, None))
    return field_values

class Stock:
    #建構子
    def __init__(self, stockId, stockName, statementdogURL=None, twseURL=None, capitalimURL=None, capitalimDate=None):
        self.stockId = stockId #string
        self.stockName = stockName #string
        self.statementdogURL = None #string,財報狗
        self.twseURL = None #string,年報
        self.capitalimURL = None #string,群益
        self.capitalimDate = None #int
        
    def Add_stock_statementdogInfo(self, statementdogURL):
        self.statementdogURL = statementdogURL
    def Add_stock_twseInfo(self, twseURL):
        self.twseURL = twseURL
    def Add_stock_capitalimInfo(self, capitalimURL, capitalimDate):
        self.capitalimURL = capitalimURL #string
        self.capitalimDate = capitalimDate #int  
    
    def Print_info(self):
        print(f"stockId:{self.stockId}, stockName:{self.stockName}, statementdogURL:{self.statementdogURL}, twseURL:{self.twseURL}, capitalimURL:{self.capitalimURL}, capitalimDate:{self.capitalimDate}")
    

def Get_listURL_simple() -> None:      #listStockId 股票代號string list, 網址含{stockId}參數 ex."https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={stockId}&year=113&mtype=F"
    for stockKey, stockValue in _dicStock.items():
        _dicStock[stockKey].Add_stock_twseInfo("https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={stockId}&year=113&mtype=F".format(stockId=stockKey))
        _dicStock[stockKey].Add_stock_statementdogInfo("https://statementdog.com/analysis/{stockId}".format(stockId=stockKey))
    
def Get_listURL_capitalim(): #listStockId 股票代號string list
    def Get_capitalim_Search_AuthToken():   
        def CreateJWT():
            header = {
                "alg": "HS256",
                "typ": "JWT"
            }
            current_time = datetime.datetime.now(datetime.timezone.utc)
            payload = {
                "id": "FrontWeb",
                "nbf": int(current_time.timestamp()),  # JWT 生效時間（現在時間）
                "exp": int((current_time + datetime.timedelta(days=1)).timestamp()),  # JWT 過期時間（1天後）
                "iat": int(current_time.timestamp())  # JWT 發行時間（現在時間）
            }
            print(int(current_time.timestamp()))
            # 生成 JWT
            jwt_token = jwt.encode(payload, '', algorithm="none", headers=header)
            print("生成的 JWT：", jwt_token)

        
        requestToken = CreateJWT()
        url = "https://www.capitalim.com.tw/cmsapi/newcms/api/Users/web/login"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": f"Bearer {requestToken}",
            "Connection": "keep-alive",
            "Cookie": "_ga=GA1.1.636061187.1720150588; G_ENABLED_IDPS=google; ASP.NET_SessionId=zquvpymlsiipkgzz5kidb3ra; TS01713f4a=01bdf56592d9ae36031d31ad481619862e7be2ddd6a10546352de49c11327aff05009eaaeb87545521941a9f1e5e48ccdf3ad15edf; _ga_HL4YRJH76V=GS1.1.1720591844.12.0.1720591852.52.0.0; TSaf2f34c4027=08763a8acdab2000d7ffd22b12d51b20c850ed2249f117f12c28454d1e1ce13f865c1d6ccc2f1b7508a00cdf47113000ebc46a7435ff9a68bf164bc5379800e6059efbe526022fc44b91a53262aa6f55ad0a22d15e6c238916da78bc4eb0bdd4",
            "Referer": "https://www.capitalim.com.tw/newsite/research-report/shares/14720;page=1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
        payload = {
            "userId": "FrontWeb",
            "password": "FrontWeb888"
        }
        response = requests.post(url, headers=headers, json=payload)
        # 檢查請求是否成功
        if response.status_code == 200:
            print("Get_capitalim_AuthToken成功:" + response.json()["token"])
            return response.json()["token"]
        else:
            print("Get_capitalim_AuthToken失敗:" + response.text)
        

    def Get_LinkURL_capitalim(authToken, stockId):   #string 股票代號
    ###取得最新報告的網址
        url = "https://www.capitalim.com.tw/cmsapi/newcms/api/IAArticle/Search?&Page=1&Take=7"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": f"Bearer {authToken}",
            "Origin": "https://www.capitalim.com.tw",
            "Referer": "https://www.capitalim.com.tw/newsite/research-report/shares;page=1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
        payload = {
            "category": "shares",
            "stockSymbol": "",  #string 股票代號
            "keyword": stockId, 
            "startDate": None,
            "endDate": None,
            "researcherName": "",
            "score": "",
            "industry": ""
        }
        response = requests.post(url, headers=headers, json=payload)

        # 檢查請求是否成功
        if response.status_code == 200:
            #解析Json
            #取最新ID
            data = json.loads(response.text)
            if 'data' in data and data['data']:
                #最新一筆資料   ##瑞昱(2379 TT)-20231023
                #find_index = data['data'][0]['titleOfContent'].find('(') 
                #name = data['data'][0]['titleOfContent'][:find_index]   #取"("之前的字元
                date = int(data['data'][0]['titleOfContent'][-8:])   #從後面取8個字元
                url_id = data['data'][0]['id']
                linkURL = "https://www.capitalim.com.tw/newsite/research-report/shares/" + str(url_id)
                print("群益研究報告:" + linkURL)                
                #_dicStock:Add_stock_capitalimInfo
                _dicStock[stockId].Add_stock_capitalimInfo(linkURL, date)
            else:
                print("No data found in the API response")
        else:
            print(f"Failed to retrieve HTML: Status code {response.status_code}")
    


    #取authToken
    authToken = Get_capitalim_Search_AuthToken()    
    #太頻繁request會被block
    i = 1 
    for stockKey, stockValue in _dicStock.items(): #key:股票代號, value:Stock Class
        if i % 15 == 0:        
            time.sleep(5) 
        Get_LinkURL_capitalim(authToken, stockKey)
        i = i + 1        

    
#修改HTML中的Table
def UpdateHTML_tblStockList_Addfield():
    
    #新增欄位
    def AddField(table, strTitle, listURL): #table, Add:標題名稱, Add:listURL網址                
        #JS:AddField
        driver.execute_script(
            """
                var tb = arguments[0];
                var strTitle = arguments[1];
                var listURL = arguments[2];
                var rows = tb.querySelectorAll('tbody > tr');
                var intUrlIndex = 0;

                rows.forEach(function(row){
                    if(row.classList.contains('bg_h2')) //標題
                    {                  
                        var clone_th = row.querySelector('th,td').cloneNode(true);
                        clone_th.querySelector('div > div').textContent = strTitle;
                        console.log(clone_th);
                        row.appendChild(clone_th);
                    }
                    else    //複製第二個th(欄位:名稱)
                    {
                        var clone_th = row.querySelector('th:nth-child(2)').cloneNode(true);
                        var element_a = clone_th.querySelector('a');
                        if(listURL[intUrlIndex])
                        {
                            element_a.href = listURL[intUrlIndex];
                        }
                        else
                        {
                            element_a.removeAttribute('href');
                            element_a.textContent = "無報告";   //修改<a>元素的文字
                        }
                        element_a.href = listURL[intUrlIndex];
                        console.log(clone_th);
                        console.log(intUrlIndex);
                        row.appendChild(clone_th);
                        intUrlIndex++;
                    }
                });
            """, table, strTitle, listURL
            )
    def AddField_EditText(table, strTitle, listURL, listDate): #table, Add:標題名稱, Add:listURL網址 , Add:編輯文字               
        #JS:AddField
        driver.execute_script(
            """
                var tb = arguments[0];
                var strTitle = arguments[1];
                var listURL = arguments[2];
                var listDate = arguments[3];
                var rows = tb.querySelectorAll('tbody > tr');
                var intUrlIndex = 0;

                rows.forEach(function(row){
                    if(row.classList.contains('bg_h2')) //標題
                    {                  
                        var clone_th = row.querySelector('th,td').cloneNode(true);
                        clone_th.querySelector('div > div').textContent = strTitle;
                        console.log(clone_th);
                        row.appendChild(clone_th);
                    }
                    else    //複製第二個th(欄位:名稱)
                    {
                        var clone_th = row.querySelector('th:nth-child(2)').cloneNode(true);
                        var element_a = clone_th.querySelector('a');
                        if(listURL[intUrlIndex])
                        {
                            element_a.href = listURL[intUrlIndex];
                            element_a.textContent = listDate[intUrlIndex] + "_" + element_a.textContent;   //修改<a>元素的文字
                        }
                        else
                        {
                            element_a.removeAttribute('href');
                            element_a.textContent = "無報告";   //修改<a>元素的文字
                        }
                        element_a.href = listURL[intUrlIndex];
                        console.log(clone_th);
                        console.log(intUrlIndex);
                        row.appendChild(clone_th);
                        intUrlIndex++;
                    }
                });
            """, table, strTitle, listURL, listDate
            )
    
    element_tb = driver.find_element(By.ID,"tblStockList")  #Table
    #Rows找股票代號存入陣列
    rows_tr = element_tb.find_elements(By.CSS_SELECTOR, "tbody > tr") #rows_tr
    i = 0
    for row in rows_tr:
        print("i" + str(i))        
        print(row.get_attribute('class'))
        #找到標題class="bg_h2"就跳過，找不到不會報錯而停止程式
        if "bg_h2" in row.get_attribute('class'):
            print("continue")
            continue
        
        # 找到第一個 <th> 元素
        first_th = row.find_element(By.CSS_SELECTOR, "th:nth-child(1)")        
        # 找到第二個 <th> 元素
        second_th = row.find_element(By.CSS_SELECTOR, "th:nth-child(2)")
        # 找到 <a> 標籤文字內容
        
        stockId = first_th.find_element(By.TAG_NAME, "a").text  #ID
        stockName = second_th.find_element(By.TAG_NAME, "a").text #名稱
        _dicStock[stockId] = Stock(stockId, stockName)
        i = i + 1

    Get_listURL_simple()
    Get_listURL_capitalim()
    for stockKey, stockValue in _dicStock.items():
        stockValue.Print_info() 
    
    AddField(element_tb, "財報狗", Get_stock_field_values(_dicStock, "statementdogURL"))
    AddField(element_tb, "年報", Get_stock_field_values(_dicStock, "twseURL"))
    AddField_EditText(element_tb, "群益報告", Get_stock_field_values(_dicStock, "capitalimURL"), Get_stock_field_values(_dicStock, "capitalimDate"))


###Selenium台股資訊網的自訂選股
#使用者
user_data_dir = r'C:\Users\Jake\AppData\Local\Google\Chrome\User Data Test'
profile_path = 'Default'  # 使用預設資料夾，也可以指定其他資料夾

# 配置 Chrome 選項
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"profile-directory={profile_path}")
service = Service(ChromeDriverManager().install())
# 啟動 ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://goodinfo.tw/tw/StockList.asp")
time.sleep(10)
UpdateHTML_tblStockList_Addfield()
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("程式中止，關閉瀏覽器。")
    driver.quit()



