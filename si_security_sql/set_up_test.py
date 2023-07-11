from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup


def sqlinjection(host):
    try:
        # create a new Chrome session
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)

        # driver.implicitly_wait(30)
        driver.maximize_window()
        print("Selenium Success")
    except:
        print("Selenium Failed")


def send_request(host):
    try:
        response = requests.get(host)
        print("Request Success")
    except:
        print("Request Failed")


def bs4_parse():
    html_doc = """<html><head><title>The Dormouse's story</title></head>
                <body>
                <p class="title"><b>The Dormouse's story</b></p>

                <p class="story">Once upon a time there were three little sisters; and their names were
                <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                and they lived at the bottom of a well.</p>

                <p class="story">...</p>
                """
    try:
        BeautifulSoup(html_doc, "html.parser")
        print("Beautiful Soup Success")
    except:
        print("Beautiful Soup Failed")


sqlinjection("http://google.com")
send_request("http://google.com")
bs4_parse()
