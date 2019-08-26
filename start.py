import os 
import time
import pytesseract
from PIL import Image, ImageOps

from models import *
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

        print('waiting for authentication, hit ENTER when ready')
        input()

        # set display size
        driver.set_window_size(1024, 768)

        # print('sleeping for 10 seconds, wait for the "enable notifications" screen to appear')
        # time.sleep(10)

        # driver.execute_script('console.log(1)')
        # keep hitting TAB until cursor is inside search box
        # while not is_search_active(driver):
        #     time.sleep(1)
        #     driver.find_element_by_tag_name('body').send_keys(Keys.TAB)

        time.sleep(2)
        while True:
            # fetch contacts from db to monitor
            for contact in _fetch_contacts():
                print(contact.name)

                # populate text field
                # driver.find_element_by_tag_name('body').send_keys("Riju")
                driver.find_element_by_css_selector('input').send_keys(contact.name)

                print('waiting for search results to load')
                time.sleep(2)
                # selecting the first search result
                driver.find_element_by_css_selector('span[title="{}"]'.format(contact.name)).click()
                print('waiting for contact details to load')
                time.sleep(3)
                # reading info
                lst = driver.find_elements_by_css_selector('div#main span')
                for _ in lst:
                    status_txt = _.get_attribute('title')
                    if status_txt != '':
                        print(status_txt)
                
                # clearing search
                driver.find_element_by_css_selector('div#side button').click()
                

            
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

def _fetch_contacts():
    session = get_session()
    try:
        return session.query(Contacts).all()
    finally:
        session.close()

if __name__ == '__main__':
    main()