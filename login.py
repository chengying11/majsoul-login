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

    print('=== Finding HTML input elements ===')
    
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='電郵'], input[placeholder*='email'], input[placeholder*='账号'], input[type='text']"))
        )
        print('Found email input element')
        
        email_input.click()
        sleep(1)
        email_input.clear()
        email_input.send_keys(email)
        print(f'Entered email: {email[:5]}***')
        
        sleep(2)
        driver.save_screenshot(f"after_email_{i+1}.png")
        print('After email screenshot saved')
        
    except Exception as e:
        print(f'Failed to find email input: {e}')
        driver.save_screenshot(f"email_error_{i+1}.png")
        driver.quit()
        raise

    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='密碼'], input[placeholder*='password'], input[type='password']"))
        )
        print('Found password input element')
        
        password_input.click()
        sleep(1)
        password_input.clear()
        password_input.send_keys(passwd)
        print(f'Entered password: {"*" * len(passwd)}')
        
        sleep(2)
        driver.save_screenshot(f"after_password_{i+1}.png")
        print('After password screenshot saved')
        
    except Exception as e:
        print(f'Failed to find password input: {e}')
        driver.save_screenshot(f"password_error_{i+1}.png")
        driver.quit()
        raise

    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'進入') or contains(text(),'登录') or contains(text(),'Login')]"))
        )
        print('Found login button')
        
        login_button.click()
        print('Clicked login button')
        
        sleep(15)
        driver.save_screenshot(f"after_login_{i+1}.png")
        print('After login screenshot saved')
        
    except Exception as e:
        print(f'Failed to find login button: {e}')
        driver.save_screenshot(f"login_button_error_{i+1}.png")
        driver.quit()
        raise

    print('Waiting for login process...')
    sleep(45)
    driver.save_screenshot(f"after_login_wait_{i+1}.png")
    print('After login wait screenshot saved')

    driver.quit()
