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

    canvas_width = screen.size['width']
    canvas_height = screen.size['height']
    print(f'Canvas center: ({canvas_width/2}, {canvas_height/2})')
    print(f'Safe offset range: x: 0-{canvas_width}, y: 0-{canvas_height}')

    print('Waiting for game to fully load...')
    sleep(60)
    print('Game load wait completed')

    driver.save_screenshot(f"login_screen_{i+1}.png")
    print('Login screen captured')

    print('=== Debug: Trying different click methods ===')
    
    print('\n--- Method 1: ActionChains with move_to_element (center) ---')
    try:
        actions = ActionChains(driver)
        actions.move_to_element(screen)
        actions.click()
        actions.perform()
        print('Success: Clicked canvas center')
    except Exception as e:
        print(f'Failed: {e}')

    sleep(1)
    
    print('\n--- Method 2: Direct click on canvas element ---')
    try:
        screen.click()
        print('Success: Direct click on canvas')
    except Exception as e:
        print(f'Failed: {e}')

    sleep(1)
    
    print('\n--- Method 3: JavaScript click at center ---')
    try:
        driver.execute_script("""
            var canvas = document.querySelector('canvas');
            if (canvas) {
                canvas.click();
            }
        """)
        print('Success: JS click on canvas')
    except Exception as e:
        print(f'Failed: {e}')

    sleep(1)
    
    print('\n--- Attempting email input ---')
    email_x = int(canvas_width * 0.7)
    email_y = int(canvas_height * 0.4)
    print(f'Target email position: ({email_x}, {email_y})')
    
    try:
        driver.execute_script(f"""
            var canvas = document.querySelector('canvas');
            if (canvas) {{
                var rect = canvas.getBoundingClientRect();
                console.log('Canvas rect:', rect);
                var x = rect.left + {email_x};
                var y = rect.top + {email_y};
                console.log('Click position:', x, y);
                var event = new MouseEvent('click', {{
                    clientX: x,
                    clientY: y,
                    bubbles: true
                }});
                canvas.dispatchEvent(event);
            }}
        """)
        print('Success: Clicked email field position')
        sleep(2)
        
        actions = ActionChains(driver)
        actions.send_keys(email)
        actions.perform()
        print(f'Success: Sent email: {email[:5]}***')
    except Exception as e:
        print(f'Failed: {e}')

    driver.save_screenshot(f"after_email_{i+1}.png")
    print('After email screenshot saved')

    sleep(3)
    
    print('\n--- Attempting password input ---')
    pass_x = int(canvas_width * 0.7)
    pass_y = int(canvas_height * 0.52)
    print(f'Target password position: ({pass_x}, {pass_y})')
    
    try:
        driver.execute_script(f"""
            var canvas = document.querySelector('canvas');
            if (canvas) {{
                var rect = canvas.getBoundingClientRect();
                var event = new MouseEvent('click', {{
                    clientX: rect.left + {pass_x},
                    clientY: rect.top + {pass_y},
                    bubbles: true
                }});
                canvas.dispatchEvent(event);
            }}
        """)
        print('Success: Clicked password field position')
        sleep(2)
        
        actions = ActionChains(driver)
        actions.send_keys(passwd)
        actions.perform()
        print(f'Success: Sent password: {"*" * len(passwd)}')
    except Exception as e:
        print(f'Failed: {e}')

    driver.save_screenshot(f"after_password_{i+1}.png")
    print('After password screenshot saved')

    sleep(3)
    
    print('\n--- Attempting login ---')
    login_x = int(canvas_width * 0.7)
    login_y = int(canvas_height * 0.68)
    print(f'Target login button position: ({login_x}, {login_y})')
    
    try:
        driver.execute_script(f"""
            var canvas = document.querySelector('canvas');
            if (canvas) {{
                var rect = canvas.getBoundingClientRect();
                var event = new MouseEvent('click', {{
                    clientX: rect.left + {login_x},
                    clientY: rect.top + {login_y},
                    bubbles: true
                }});
                canvas.dispatchEvent(event);
            }}
        """)
        print('Success: Clicked login button')
    except Exception as e:
        print(f'Failed: {e}')

    sleep(10)
    driver.save_screenshot(f"after_login_{i+1}.png")
    print('After login screenshot saved')

    driver.quit()
