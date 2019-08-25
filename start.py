import os 
import time
import pytesseract
from PIL import Image, ImageOps

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    try:
        chrome_options = Options()  
        # chrome_options.add_argument("--headless")  # toggle this for headless
        # chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

        driver = webdriver.Chrome(
            executable_path=os.path.abspath("utils/chromedriver"),
            chrome_options=chrome_options
            )  

        # launch whatsapp web
        driver.get("https://web.whatsapp.com")

        print('waiting for authentication')
        input()

        # set display size
        driver.set_window_size(1024, 768)

        print('sleeping for 10 seconds, wait for the "enable notifications" screen to appear')
        time.sleep(10)

        driver.execute_script('console.log(1)')
        driver.find_element_by_css_selector('input').click()
        # keep hitting TAB until cursor is inside search box
        # while not is_search_active(driver):
        #     time.sleep(1)
        #     driver.find_element_by_tag_name('body').send_keys(Keys.TAB)

        # populate text field
        driver.find_element_by_tag_name('body').send_keys("Riju")

        input()
        # 'Get notified of new messages\nTurn on desktop notifications »'


        numbers_lst = [
            '9654560437',
            '9025078945',
            ]
    finally:
        driver.quit()


def is_search_active(driver):
    time.sleep(2)
    # check if "search or start new chat" exist in image
    driver.save_screenshot("img/ww.png")
    # ImageOps.crop(Image.open('img/ww.png'), (0, 650, 120, 0)).save('img/notif.png')

    ImageOps.crop(Image.open('img/ww.png'), (50, 150, 750, 450)).save('img/search.png')
    search_txt = pytesseract.image_to_string(Image.open('img/search.png'))
    # print(search_txt)
    
    print(search_txt)
    for word in ['Search', 'or', 'start', 'new', 'chat']:
        if word in search_txt:
            print(word)
            return False

    return True

if __name__ == '__main__':
    main()