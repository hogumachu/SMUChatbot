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

def professor_info(request):
    name = request.GET['pi']
    print(name)
    pi = professor(name)
    print(pi)
    context = {'pi':pi}
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
            result += "email : " + k[0][16:] + '<br> <br>'
        elif "소속 :" in l:
            result += l + '<br> <br>'
        elif "전화 :" in l:
            result += l + '<br> <br>'
        elif "위치 :" in l:
            result += l + '<br> <br> <br>'
    return str(''.join(result))