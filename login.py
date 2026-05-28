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

    print('\n=== Debug: Page Structure Analysis ===')
    
    print('\n1. Checking for iframes...')
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f'Found {len(iframes)} iframes')
    for idx, iframe in enumerate(iframes):
        print(f'  Iframe {idx}: name="{iframe.get_attribute("name")}", src="{iframe.get_attribute("src")[:50]}..."')

    print('\n2. Checking all input elements on main page...')
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f'Found {len(inputs)} input elements')
    for idx, inp in enumerate(inputs):
        placeholder = inp.get_attribute("placeholder")
        type_attr = inp.get_attribute("type")
        print(f'  Input {idx}: type="{type_attr}", placeholder="{placeholder}"')

    print('\n3. Checking document body HTML (first 1000 chars)...')
    body_html = driver.execute_script("return document.body.innerHTML")[:1000]
    print(body_html)

    print('\n=== Attempting to switch to iframe and find inputs ===')
    for idx, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            print(f'Switched to iframe {idx}')
            
            iframe_inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f'Found {len(iframe_inputs)} input elements in iframe {idx}')
            for j, inp in enumerate(iframe_inputs):
                placeholder = inp.get_attribute("placeholder")
                type_attr = inp.get_attribute("type")
                print(f'  Input {j}: type="{type_attr}", placeholder="{placeholder}"')
            
            driver.switch_to.default_content()
        except Exception as e:
            print(f'Failed to switch to iframe {idx}: {e}')
            driver.switch_to.default_content()

    driver.quit()
