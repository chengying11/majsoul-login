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
    driver.set_window_size(1280, 800)  # 增大窗口尺寸
    driver.get("https://game.maj-soul.net/1/")
    print(f'Account {i+1} loading game...')
    sleep(15)  # 增加初始加载等待时间

    # 2. 等待游戏画布加载
    try:
        screen = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print(f'Canvas found, size: {screen.size}')
    except:
        driver.save_screenshot(f"error_{i+1}.png")
        driver.quit()
        raise

    # 保存登录界面截图
    driver.save_screenshot(f"login_screen_{i+1}.png")
    print('Login screen captured')

    # 3. 输入账号
    # 尝试不同的坐标位置来定位输入框
    print('Trying to input email...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 280, -80)\
        .click()\
        .send_keys(email)\
        .perform()
    sleep(2)
    print('Email input attempted')

    # 4. 输入密码
    print('Trying to input password...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 280, -20)\
        .click()\
        .send_keys(passwd)\
        .perform()
    sleep(2)
    print('Password input attempted')

    # 保存输入后截图
    driver.save_screenshot(f"after_input_{i+1}.png")
    print('Input screen captured')

    # 5. 点击登录
    print('Clicking login button...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 280, 60)\
        .click()\
        .perform()
    print('Login button clicked')
    sleep(30)  # 等待游戏加载完成
    print('Login success')

    # 6. 领取月卡
    print('Attempting to claim monthly card...')
    sleep(5)
    
    # 第一次点击
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 0, 50)\
        .click()\
        .perform()
    sleep(2)
    
    # 第二次点击
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 0, 50)\
        .click()\
        .perform()
    sleep(2)
    
    print('Monthly card claim attempt completed')
    
    # 保存结果截图
    driver.save_screenshot(f"result_{i+1}.png")
    print(f'Screenshot saved as result_{i+1}.png')
    
    driver.quit()
