import urllib.request
import requests
import urllib.parse
from bs4 import BeautifulSoup

def professor(name):
    readUrl = "https://www.smu.ac.kr/search/search.do?menu=교수검색&qt=" + name
    url = requests.get(readUrl).text.encode('utf-8')
    soup = BeautifulSoup(url, 'html.parser')

    pkg_list = soup.findAll("ul", "list4 staff")
    p = str(pkg_list).split('\t')
    result = []
    for l in p:
        if  "mailto" in l:
            k = l.split('">')
            result += "email : " + k[0][16:] + "\n"
        elif "소속 :" in l:
            result += l
        elif "전화 :" in l:
            result += l
        elif "위치 :" in l:
            result += l + '\n'
    print(''.join(result))

