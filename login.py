import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

acccounts = int(len(sys.argv[1:])/2)
print(f'Config {acccounts} accounts')
for i in range(acccounts):
    email = sys.argv[1+i]
    passwd = sys.argv[1+i+acccounts]
    print('----------------------------')

    # 1. 打开浏览器（反风控配置，必须保留）
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1000, 720)
    driver.get("https://game.maj-soul.net/1/")
    print(f'Account {i+1} loading game...')
    sleep(10)

    # 2. 等待游戏画布加载（修复找不到元素）
    try:
        screen = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
    except:
        driver.save_screenshot(f"error_{i+1}.png")
        driver.quit()
        raise

    # 3. 点击账号输入框 + 直接输入（核心修复：删除了错误的find_element）
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, -100)\
        .click()\
        .perform()
    sleep(1)
    driver.send_keys(email)  # 直接模拟键盘输入，不需要找input元素
    print('Input email successfully')

    # 4. 点击密码输入框 + 直接输入（核心修复：删除了错误的find_element）
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, -50)\
        .click()\
        .perform()
    sleep(1)
    driver.send_keys(passwd)
    print('Input password successfully')

    # 5. 点击登录
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, 50)\
        .click()\
        .perform()
    print('Entering game...')
    sleep(20)
    print('Login success')
    driver.quit()
