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
    
    # 3. 等待游戏资源加载完成（出现登录界面）
    # 等待更长时间，直到登录界面完全加载
    max_wait = 90  # 最多等待90秒
    wait_interval = 10  # 每10秒检查一次
    waited = 0
    
    print('Waiting for game to fully load...')
    while waited < max_wait:
        sleep(wait_interval)
        waited += wait_interval
        driver.save_screenshot(f"loading_check_{i+1}_{waited}.png")
        print(f'  Checked at {waited}s')
        
        # 等待60秒后尝试输入
        if waited >= 60:
            break
    
    print(f'Waited {waited}s for game load')
    
    # 保存登录界面截图
    driver.save_screenshot(f"login_screen_{i+1}.png")
    print('Login screen captured')

    # 4. 输入账号 - 使用JavaScript直接设置值可能更可靠
    print('Trying to input email...')
    # 先点击激活输入框
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 280, -80)\
        .click()\
        .perform()
    sleep(1)
    # 清除并输入
    ActionChains(driver)\
        .key_down('ctrl')\
        .key_down('a')\
        .key_up('a')\
        .key_up('ctrl')\
        .perform()
    sleep(0.5)
    ActionChains(driver)\
        .send_keys(email)\
        .perform()
    sleep(2)
    print('Email input attempted')

    # 5. 输入密码
    print('Trying to input password...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 280, -20)\
        .click()\
        .perform()
    sleep(1)
    ActionChains(driver)\
        .key_down('ctrl')\
        .key_down('a')\
        .key_up('a')\
        .key_up('ctrl')\
        .perform()
    sleep(0.5)
    ActionChains(driver)\
        .send_keys(passwd)\
        .perform()
    sleep(2)
    print('Password input attempted')

    # 保存输入后截图
    driver.save_screenshot(f"after_input_{i+1}.png")
    print('Input screen captured')

    # 6. 点击登录
    print('Clicking login button...')
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 280, 60)\
        .click()\
        .perform()
    print('Login button clicked')
    sleep(40)  # 等待游戏加载完成
    print('Login success')

    # 7. 领取月卡
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
