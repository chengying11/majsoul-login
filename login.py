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

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://game.maj-soul.net/1/")
    print(f'Account {i+1} loading game...')
    
    try:
        screen = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print(f'Canvas found, size: {screen.size}')
    except:
        driver.save_screenshot(f"error_canvas_{i+1}.png")
        driver.quit()
        raise
    
    print('Waiting for game to fully load...')
    sleep(60)
    print('Game load wait completed')
    
    driver.save_screenshot(f"login_screen_{i+1}.png")
    print('Login screen captured')

    print('Trying to input email...')
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[placeholder*='账号'], input[placeholder*='email'], input[name*='email']"))
        )
        email_input.click()
        email_input.send_keys(email)
        print('Email input attempted')
    except Exception as e:
        print(f'Email input failed: {e}')
        driver.save_screenshot(f"email_input_error_{i+1}.png")
        driver.quit()
        raise

    driver.save_screenshot(f"after_email_{i+1}.png")
    print('After email input captured')

    print('Trying to input password...')
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.click()
        password_input.send_keys(passwd)
        print('Password input attempted')
    except Exception as e:
        print(f'Password input failed: {e}')
        driver.save_screenshot(f"password_input_error_{i+1}.png")
        driver.quit()
        raise

    driver.save_screenshot(f"after_password_{i+1}.png")
    print('After password input captured')

    print('Clicking login button...')
    try:
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'登录')] | //div[contains(@class,'login')]//button | //a[contains(text(),'登录')]"))
        )
        login_btn.click()
        print('Login button clicked')
    except Exception as e:
        print(f'Login button click failed: {e}')
        try:
            ActionChains(driver).send_keys('\n').perform()
            print('Pressed Enter as fallback')
        except:
            pass

    sleep(15)
    
    driver.save_screenshot(f"after_login_click_{i+1}.png")
    print('After login click captured')

    print('Waiting for login process...')
    sleep(45)
    
    driver.save_screenshot(f"after_login_wait_{i+1}.png")
    print('After login wait captured')

    print('Checking for server selection...')
    sleep(5)
    
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'close')] | //div[contains(@class,'modal')]//button | //span[contains(@class,'close')]"))
        )
        close_btn.click()
        print('Closed dialog')
    except:
        print('No dialog to close or close failed')
        try:
            ActionChains(driver).send_keys('\n').perform()
        except:
            pass

    driver.save_screenshot(f"after_server_select_{i+1}.png")
    print('After server select captured')

    print('Waiting for game entry...')
    sleep(30)

    print('Attempting to claim monthly card...')
    try:
        claim_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'领取')] | //div[contains(@class,'monthly')]//button"))
        )
        claim_btn.click()
        sleep(2)
        try:
            claim_btn.click()
        except:
            pass
        print('Monthly card claim attempt completed')
    except Exception as e:
        print(f'Monthly card claim failed: {e}')
    
    driver.save_screenshot(f"result_{i+1}.png")
    print(f'Screenshot saved as result_{i+1}.png')
    
    driver.quit()
