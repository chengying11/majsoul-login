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

    # 1. 浏览器配置（反风控，GitHub必备）
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 800)
    driver.get("https://game.maj-soul.net/1/")
    print(f'Account {i+1} loading game...')
    
    # 2. 等待游戏画布加载
    try:
        screen = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print(f'Canvas found, size: {screen.size}')
    except:
        driver.save_screenshot(f"error_canvas_{i+1}.png")
        driver.quit()
        raise
    
    # 3. 等待游戏资源加载完成
    print('Waiting for game to fully load...')
    sleep(60)
    print('Game load wait completed')
    
    driver.save_screenshot(f"login_screen_{i+1}.png")
    print('Login screen captured')

    # 4. 输入账号 - 调整坐标
    print('Trying to input email...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 300, -130)\
        .click()\
        .send_keys(email)\
        .perform()
    sleep(2)
    print('Email input attempted')

    # 5. 输入密码 - 调整坐标
    print('Trying to input password...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 300, -50)\
        .click()\
        .send_keys(passwd)\
        .perform()
    sleep(2)
    print('Password input attempted')

    driver.save_screenshot(f"after_input_{i+1}.png")
    print('Input screen captured')

    # 6. 点击登录
    print('Clicking login button...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 300, 30)\
        .click()\
        .perform()
    print('Login button clicked')
    sleep(5)
    
    # 7. 关闭服务器选择弹窗（如果出现）
    driver.save_screenshot(f"before_close_{i+1}.png")
    print('Checking for server selection dialog...')
    
    # 点击关闭按钮位置（弹窗右上角）
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 300, -200)\
        .click()\
        .perform()
    sleep(2)
    
    # 等待进入游戏
    sleep(35)
    print('Login success')

    # 8. 领取月卡
    print('Attempting to claim monthly card...')
    sleep(5)
    
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 0, 50)\
        .click()\
        .perform()
    sleep(2)
    
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 0, 50)\
        .click()\
        .perform()
    sleep(2)
    
    print('Monthly card claim attempt completed')
    
    driver.save_screenshot(f"result_{i+1}.png")
    print(f'Screenshot saved as result_{i+1}.png')
    
    driver.quit()
