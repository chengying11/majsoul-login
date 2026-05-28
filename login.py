import sys
from time import sleep

from selenium import webdriver
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

    def simulate_click(x, y):
        driver.execute_script(f'''
            var canvas = document.querySelector('canvas');
            if (canvas) {{
                var rect = canvas.getBoundingClientRect();
                var clickEvent = new MouseEvent('click', {{
                    clientX: rect.left + {x},
                    clientY: rect.top + {y},
                    bubbles: true,
                    cancelable: true
                }});
                canvas.dispatchEvent(clickEvent);
            }}
        ''')

    def simulate_keyboard(text):
        driver.execute_script(f'''
            var canvas = document.querySelector('canvas');
            if (canvas) {{
                text.split('').forEach(function(char) {{
                    var keyEvent = new KeyboardEvent('keydown', {{
                        key: char,
                        bubbles: true,
                        cancelable: true
                    }});
                    canvas.dispatchEvent(keyEvent);
                    keyEvent = new KeyboardEvent('keypress', {{
                        key: char,
                        bubbles: true,
                        cancelable: true
                    }});
                    canvas.dispatchEvent(keyEvent);
                    keyEvent = new KeyboardEvent('keyup', {{
                        key: char,
                        bubbles: true,
                        cancelable: true
                    }});
                    canvas.dispatchEvent(keyEvent);
                }});
            }}
        ''', text)

    print('Trying to input email...')
    simulate_click(900, 280)
    sleep(1)
    simulate_keyboard(email)
    sleep(2)
    print('Email input attempted')

    driver.save_screenshot(f"after_email_{i+1}.png")
    print('After email input captured')

    print('Trying to input password...')
    simulate_click(900, 360)
    sleep(1)
    simulate_keyboard(passwd)
    sleep(2)
    print('Password input attempted')

    driver.save_screenshot(f"after_password_{i+1}.png")
    print('After password input captured')

    print('Clicking login button...')
    simulate_click(900, 480)
    print('Login button clicked')
    sleep(15)

    driver.save_screenshot(f"after_login_click_{i+1}.png")
    print('After login click captured')

    print('Waiting for login process...')
    sleep(45)

    driver.save_screenshot(f"after_login_wait_{i+1}.png")
    print('After login wait captured')

    print('Checking for server selection...')
    sleep(5)

    simulate_click(900, 200)
    sleep(5)

    driver.save_screenshot(f"after_server_select_{i+1}.png")
    print('After server select captured')

    print('Waiting for game entry...')
    sleep(30)

    print('Attempting to claim monthly card...')
    simulate_click(640, 560)
    sleep(3)
    simulate_click(640, 560)
    sleep(3)
    print('Monthly card claim attempt completed')

    driver.save_screenshot(f"result_{i+1}.png")
    print(f'Screenshot saved as result_{i+1}.png')

    driver.quit()
