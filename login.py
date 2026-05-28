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

    # 1. 浏览器配置（反风控）
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

    # 2. 等待游戏画布加载
    try:
        screen = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
    except:
        driver.save_screenshot(f"error_{i+1}.png")
        driver.quit()
        raise

    # 3. 输入账号（修复：正确的Canvas输入方式）
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, -100)\
        .click()\
        .send_keys(email)\
        .perform()
    sleep(1)
    print('Input email successfully')

    # 4. 输入密码（修复：正确的Canvas输入方式）
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, -50)\
        .click()\
        .send_keys(passwd)\
        .perform()
    sleep(1)
    print('Input password successfully')

    # 5. 点击登录
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 250, 50)\
        .click()\
        .perform()
    print('Entering game...')
    sleep(30)  # 增加等待时间，等待游戏加载完成
    print('Login success')

    # 6. 领取月卡 - 月卡弹窗会在登录后自动显示在中间，直接点击即可
    print('Attempting to claim monthly card...')
    sleep(5)  # 等待月卡弹窗出现
    
    # 第一次点击 - 打开月卡弹窗或点击领取
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 0, 50)\
        .click()\
        .perform()
    sleep(2)
    
    # 第二次点击 - 确认领取或关闭弹窗
    ActionChains(driver)\
        .move_to_element_with_offset(screen, 0, 50)\
        .click()\
        .perform()
    sleep(2)
    
    print('Monthly card claim attempt completed')
    
    # 保存截图以便调试
    driver.save_screenshot(f"result_{i+1}.png")
    print(f'Screenshot saved as result_{i+1}.png')
    
    driver.quit()
