'''
Database is a collection of tables and user information is stored in a table called <users>. 
The goal of this assignment is finding the database name. You will need to follow steps below to be graded.

0. create and activate a virtual enviroment (https://docs.python.org/3/library/venv.html)
1. install the requirements (pip install -r requirements.txt)
2. find the length of database name
3. find the database name
4. create a db_name.log file in the same directory as your script
5. db_name.log format should be as below

<Your name>
The length of DB name : <answer>
The name of DB: <answer>

e.g.
Jonghyeok Kim
The length of DB name : 10
The name of DB: mydatabase

6. submit your sqli_<your_name>.py

e.g.
sqli_jonghyeok_kim.py
db_name.log

Remove the above for your answer
'''

import requests
from bs4 import BeautifulSoup
from pathlib import Path

LIMIT = 100
PHPSESSID = "2q7sgh6jm4lrl5jamh53msagg2"  # 0. Replace with your session
SECURITY = "high"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
          "Accept-Encoding": "gzip, deflate",
          "Accept-Language": "en-US,en;q=0.9",
          "Connection": "close",
          "Upgrade-Insecure-Requests": "1"}


def get_db_name_len() -> int:
    '''Send a SQL attack and get the length of the db name'''
    db_name_len = 0
    # Loop until SQL command return True. Try untill 100. If not found, raise an error
    while True:
        db_name_len += 1
        url = f"http://localhost/vulnerabilities/sqli_blind/"
        # 1. set up cookies and send a request to do SQL attack to get the DB name length
        cookies = {"PHPSESSID": PHPSESSID, "security": SECURITY}
        response = requests.post(url, cookies=cookies)

        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        # 2. If respond returns True, return the DB name length value
        # if
        #     return
        if db_name_len > 100:
            raise ValueError(
                f'Tried {db_name_len} time but table len not found')


def get_db_name_char_ascii(digit: int) -> str:
    '''Send a SQL attack and get a charater of the db name at position {digit}'''
    target_ascii = 96
    while True:
        target_ascii += 1
        url = f"http://localhost/vulnerabilities/sqli_blind/"
        # 3. set up cookies and send a request to do SQL attack to get the a character of DB name
        # cookies =
        # response = requests.

        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        # 4. If respond returns True, return the character
        # if
        #     return
        if target_ascii > 122:
            raise ValueError(f'char not found on {digit}')


def get_db_name(name_len: int) -> str:
    db_name = ""
    for idx in range(1, name_len + 1):
        db_name += get_db_name_char_ascii(idx)
    output_file = Path(__file__).with_name('db_name.log')
    fp = open(output_file, 'w')
    fp.write(f"Jonghyeok Kim\n")  # 5. Replace with your name
    fp.write(f"The length of DB name : {name_len}\n")
    fp.write(f"The name of DB: {db_name}\n")
    fp.close()
    return db_name


if __name__ == "__main__":
    db_name_len = get_db_name_len()
    print(db_name_len)
    db_name = get_db_name(db_name_len)
    print(db_name)
