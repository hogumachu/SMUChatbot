
import urllib3
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url="https://www.smu.ac.kr/search/search.do?menu=%EA%B5%90%EC%88%98%EA%B2%80%EC%83%89&qt=%ED%95%9C%ED%98%81%EC%88%98"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

pkg_list=soup.findAll("ul", "list4 staff")
for i in pkg_list:
    email = i.findAll('a')
    print ("email :",str(email)[str(email).find('href="mailto:')+13:str(title).find('">')])