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

    canvas_width = screen.size['width']
    canvas_height = screen.size['height']
    print(f'Canvas dimensions: {canvas_width}x{canvas_height}')

    print('Waiting for game to fully load...')
    sleep(60)
    print('Game load wait completed')

    driver.save_screenshot(f"login_screen_{i+1}.png")
    print('Login screen captured')

    def click_at(x, y):
        driver.execute_script(f"""
            var canvas = document.querySelector('canvas');
            if (canvas) {{
                var rect = canvas.getBoundingClientRect();
                var evt = new MouseEvent('mousedown', {{clientX: rect.left + {x}, clientY: rect.top + {y}, bubbles: true}});
                canvas.dispatchEvent(evt);
                evt = new MouseEvent('mouseup', {{clientX: rect.left + {x}, clientY: rect.top + {y}, bubbles: true}});
                canvas.dispatchEvent(evt);
                evt = new MouseEvent('click', {{clientX: rect.left + {x}, clientY: rect.top + {y}, bubbles: true}});
                canvas.dispatchEvent(evt);
            }}
        """)

    def type_text(text):
        driver.execute_script("""
            var canvas = document.querySelector('canvas');
            if (canvas) {
                var text = arguments[0];
                for (var i = 0; i < text.length; i++) {
                    var char = text[i];
                    var keydown = new KeyboardEvent('keydown', {key: char, bubbles: true});
                    var keypress = new KeyboardEvent('keypress', {key: char, bubbles: true});
                    var keyup = new KeyboardEvent('keyup', {key: char, bubbles: true});
                    canvas.dispatchEvent(keydown);
                    canvas.dispatchEvent(keypress);
                    canvas.dispatchEvent(keyup);
                }
            }
        """, text)

    email_x = int(canvas_width * 0.78)
    email_y = int(canvas_height * 0.42)
    print(f'\nClicking email field at ({email_x}, {email_y})...')
    click_at(email_x, email_y)
    sleep(2)
    print(f'Typing email: {email[:5]}***')
    type_text(email)
    sleep(2)
    driver.save_screenshot(f"after_email_{i+1}.png")
    print('After email screenshot saved')

    pass_x = int(canvas_width * 0.78)
    pass_y = int(canvas_height * 0.53)
    print(f'\nClicking password field at ({pass_x}, {pass_y})...')
    click_at(pass_x, pass_y)
    sleep(2)
    print(f'Typing password: {"*" * len(passwd)}')
    type_text(passwd)
    sleep(2)
    driver.save_screenshot(f"after_password_{i+1}.png")
    print('After password screenshot saved')

    login_x = int(canvas_width * 0.78)
    login_y = int(canvas_height * 0.68)
    print(f'\nClicking login button at ({login_x}, {login_y})...')
    click_at(login_x, login_y)
    sleep(15)
    driver.save_screenshot(f"after_login_{i+1}.png")
    print('After login screenshot saved')

    print('\nWaiting for login process...')
    sleep(45)
    driver.save_screenshot(f"after_login_wait_{i+1}.png")
    print('After login wait screenshot saved')

    driver.quit()
