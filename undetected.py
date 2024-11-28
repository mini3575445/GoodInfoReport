import undetected_chromedriver as uc
import time

# 初始化 ChromeDriver
options = uc.ChromeOptions()
# 設定 Chrome 使用者資料路徑
user_data_dir = r'C:\Users\Jake\AppData\Local\Google\Chrome\User Data'
profile_path = 'Default'  # 使用預設資料夾，也可以指定其他資料夾

options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"profile-directory={profile_path}")

driver = uc.Chrome(options=options)

# 開啟蝦皮登入頁面
driver.get('https://shopee.tw/buyer/login')

# 等待頁面加載
time.sleep(10)  # 你可以根據需要調整等待時間

# 在這裡你可以手動登入，或者使用 Selenium 填寫登入表單
# 例如：
# username_input = driver.find_element_by_name("loginKey")
# password_input = driver.find_element_by_name("password")
# login_button = driver.find_element_by_xpath("//button[contains(@class, 'btn-login')]")

# username_input.send_keys("你的帳號")
# password_input.send_keys("你的密碼")
# login_button.click()


# 驗證是否已登入（可以檢查頁面中的某些元素）
if "你的帳號" in driver.page_source:
    print("已成功使用現有的 Google 帳號登入")
else:
    print("未登入或登入失敗")

# 其他操作
# ...

# 關閉瀏覽器
driver.quit()
