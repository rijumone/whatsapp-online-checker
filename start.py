import os 

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()  
# chrome_options.add_argument("--headless")  # toggle this for headless
# chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

driver = webdriver.Chrome(executable_path=os.path.abspath("utils/chromedriver"),chrome_options=chrome_options)  
driver.get("https://web.whatsapp.com")

numbers_lst = [
    '9654560437',
    '9025078945',
    ]

driver.quit()