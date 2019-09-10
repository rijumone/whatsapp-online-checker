import os 
import time
import datetime
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
        # options = Options()  
        # chrome_options.add_argument("--headless")  # toggle this for headless
        # chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

        driver = webdriver.Chrome(
            executable_path=os.path.abspath("utils/chromedriver"),
            # options=options,
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
                print('\n=============\tsearching name:\t', contact.name)

                # populate text field
                # driver.find_element_by_tag_name('body').send_keys("Riju")
                driver.find_element_by_css_selector('input').send_keys(contact.name)

                print('waiting for search results to load: 2 + 10 seconds')
                time.sleep(2)
                # selecting the first search result
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title="{}"]'.format(contact.name)))
                        ).click()
                except Exception as e:
                    print('exc while attempting click on search result for:', contact.name)
                    print(e)
                    continue

                # driver.find_element_by_css_selector('span[title="{}"]'.format(contact.name)).click()
                print('waiting for contact details to load: 4 + 0 seconds')
                time.sleep(4)
                # reading info
                lst = driver.find_elements_by_css_selector('div#main span')
                for _ in lst:
                    status_txt = None
                    try:
                        status_txt = _.get_attribute('title')
                    except Exception as e:
                        print('err while fetching "title" for "div#main span"', e)
                    if status_txt not in [None, '', contact.name]:
                        print('status: ', status_txt)
                        # save this to db
                        _save_status(contact.id, status_txt)
                
                # clearing search
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#side button'))
                        ).click()
                except Exception as e:
                    print('exc while attempting clear search input:', e)
                    break
                # driver.find_element_by_css_selector('div#side button').click()
                

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

def _save_status(c_id, status):
    session = get_session()
    try:
        history = History(contact_id=c_id, status=status, timestamp=datetime.datetime.now())
        if not _is_history_redundant(c_id, status):
            session.add(history)
            session.commit()
    except Exception as e:
        print('exc while _save_status(): ', e)
    finally:
        session.close()

def _fetch_contacts():
    session = get_session()
    try:
        return session.query(Contacts).filter(Contacts.is_active==True).all()
    finally:
        session.close()

def _is_history_redundant(c_id, status):
    session = get_session()
    try:
        try:
            history = session.query(History).filter(History.contact_id==c_id, History.status==status).order_by(History.timestamp.desc()).limit(1).one()
        except Exception as e:
            print('exc while _is_history_redundant(): ', e)    
            return False
        if history is not None and 'last seen' in history.status:
            return True
    except Exception as e:
        print('exc while _is_history_redundant(): ', e)
    finally:
        session.close()
    return False

if __name__ == '__main__':
    main()