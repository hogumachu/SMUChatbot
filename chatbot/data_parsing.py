import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url="https://www.smu.ac.kr/search/search.do?menu=%EA%B5%90%EC%88%98%EA%B2%80%EC%83%89&qt=%ED%95%9C%ED%98%81%EC%88%98"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

pkg_list=soup.findAll("ul", "list4 staff")
p = str(pkg_list).split('\t')

for l in p:
    if "mailto" in l:
        k = l.split('">')
        print("email : "+k[0][16:]+"\n")
    elif "소속 :" in l:
        print(l)
    elif "전화 :" in l:
        print(l)
    elif "위치 :" in l:
        print(l+"\n")