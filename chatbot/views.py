import json
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.


def home(request):
    context = {}
    return render(request, "chathome.html", context)

def get_info(request):
    name = request.GET['data']
    print(name)
    if '역사' in name or '콘텐츠' in name or '역콘' in name:
        name = 'history'
        data = office(name)
    elif '지적' in name or '재산권' in name or '지재' in name:
        name = 'cr'
        data = office(name)
    elif '문헌' in name or '문정' in name:
        name = 'libinfo'
        data = office(name)
    elif '공간' in name or '환경학' in name or '공환' in name:
        name = 'space'
        data = office(name)
    elif '행정학' in name:
        name = 'public'
        data = office(name)
    elif '가족' in name or '복지' in name or '가복' in name:
        name = 'smfamily'
        data = office(name)
    elif '국가' in name or '안보' in name or '국안' in name:
        name = 'ns'
        data = office(name)
    elif '국어' in name or '국교' in name:
        name = 'koredu'
        data = office(name)
    elif '영어' in name or '영교' in name:
        name = 'engedu'
        data = office(name)
    elif '수학' in name or '수교' in name:
        name = 'mathedu'
        data = office(name)
    elif '교육학' in name:
        name = 'peda'
        data = office(name)
    elif '경제' in name or '금융' in name or '경금' in name:
        name = 'econo'
        data = office(name)
    elif '글로벌' in name or '글경' in name or '경금' in name:
        name = ''
        data = office(name)
    elif '융합경영' in name or '융경' in name:
        name = 'imgmt'
        data = office(name)
    elif '경영' in name:
        name = 'smubiz'
        data = office(name)
    elif '휴먼' in name or '휴지' in name:
        name = 'hi'
        data = office(name)
    elif '핀테크' in name:
        name = 'fbs'
        data = office(name)
    elif '빅데이터' in name:
        name = 'fbs'
        data = office(name)
    elif '스마트' in name or '스생' in name:
        name = 'fbs'
        data = office(name)
    elif '컴퓨터' in name or '컴과' in name or '컴공' in name:
        name = 'cs'
        data = office(name)
    elif '전기' in name:
        name = 'electric'
        data = office(name)
    elif '지능' in name or 'IOT' in name:
        name = 'aiot'
        data = office(name)
    elif '게임' in name or '겜' in name:
        name = 'game'
        data = office(name)
    elif '애니' in name:
        name = 'animation'
        data = office(name)
    elif '한일' in name or '한콘' in name or '한문' in name:
        name = 'kjc'
        data = office(name)
    elif '생명' in name or '생공' in name:
        name = 'biotechnology'
        data = office(name)
    elif '화학' in name or '화에' in name:
        name = 'energy'
        data = office(name)
    elif '화공' in name or '신소재' in name:
        name = 'ichem'
        data = office(name)
    else:
        data = professor(name)
    print(name)
    context = {'data':data}
    return JsonResponse(context)

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
            result += "<div style='margin:15px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:5px 8px;border-radius:8px;'>" + k[0][16:] + "</span> </div>"
        elif "소속 :" in l:
            result += "<div style='margin:15px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:5px 8px;border-radius:8px;'>" + l + "</span> </div>"
        elif "전화 :" in l:
            result += "<div style='margin:15px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:5px 8px;border-radius:8px;'>" + l + "</span> </div>"
        elif "위치 :" in l:
            result += "<div style='margin:15px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:5px 8px;border-radius:8px;'>" + l + "</span> </div>  <br>"

    return str(''.join(result))

def office(name):
    readUrl = "https://"+name+".smu.ac.kr/"+name+"/intro/office.do"
    url = requests.get(readUrl).text.encode('utf-8')
    soup = BeautifulSoup(url, 'html.parser')

    pkg_list = soup.findAll("ul", "ul-type01")
    p = str(pkg_list).split('<li>')
    result = []
    for l in p:
        l = l.replace("</li>", "").replace("</a>", "").replace("</ul>", "").replace("]", "").replace("\t", "").strip()
        if "ul class" in l:
            False
        elif "<" in l:
            while l.find('<') != -1:
                l = l.replace(l[l.find('<'):l.find('>') + 1], "")
            result += "<div style='margin:15px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:5px 8px;border-radius:8px;'>" + l + "</span> </div>"
        else:
            result += "<div style='margin:15px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:5px 8px;border-radius:8px;'>" + l + "</span> </div>"
    return str(''.join(result))