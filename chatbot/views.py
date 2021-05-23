import json
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import Datetoevent, Eventtodate, Officeinfo
from django.http import HttpResponse
# Create your views here.

def home(request):
    context = {}
    return render(request, "chathome.html", context)

def get_info(request):
    text = request.GET['data']
    print(text)
    data = professor(text)
    print(data)
    context = {'data':data}
    print(date_to_event(text))
    print(event_to_date(convert_event(text)))
    print(office_info(convert_office(text)))
    print(convert_office(text))
    return JsonResponse(context)




def convert_event(eventString):
    return ""

def convert_date(dateString):
    return ""

def convert_office(name):
    if '가족' in name or '가복' in name:
        return '가족복지학과'
    elif '게임' in name :
        return '게임전공'
    elif '글경' in name or '글경' in name or '글로벌경영' in name or '글로벌 경영' in name:
        return '글로벌경영학과'
    elif '융경' in name or '융합경영' in name or '융합 경영' in name:
        return '융합경영학과'
    elif '경영' in name:
        return '경영학부'
    elif '경제' in name or '경금' in name or '금융' in name:
        return '경제금융학부'
    elif '공간' in name or '환경' in name or '공환' in name:
        return '공간환경학부'
    elif '교직' in name :
        return '교직지원센터'
    elif '국가' in name or '안보' in name or '국안' in name:
        return '국가안보학과'
    elif '글로벌랭귀지' in name or '글로벌 랭귀지' in name or '글로벌 센터' in name:
        return '글로벌랭귀지센터'
    elif '일자리' in name or '대학일자리' in name or '대학 일자리' in name:
        return '대학일자리센터'
    elif '디자인' in name:
        return '디자인센터'
    elif '아트' in name:
        return '상명아트센터'
    elif '기획' in name or '예산' in name:
        return '기획예산팀'
    elif '무용' in name or '무예' in name:
        return '무용예술전공'
    elif '생활' in name or '생예' in name and '생활관' not in name:
        return '생활예술전공'
    elif '문헌' in name or '문정' in name:
        return '문헌정보학전공'
    elif '박물관' in name:
        return '박물관'
    elif '생명' in name or '생공' in name:
        return '생명공학전공'
    elif '식품' in name or '영양' in name or '식영' in name:
        return '식품영양학전공'
    elif '신문' in name or '방송' in name or '신방' in name:
        return '신문방송국'
    elif '애니' in name:
        return '애니'
    elif '역사' in name or '역콘' in name:
        return '역사콘텐츠전공'
    elif '예비군' in name:
        return '예비군대대'
    elif '외국인' in name or '유학생'in name:
        return '외국인유학생상담센터'
    elif '우편' in name:
        return '우편취급국'
    elif '음악' in name:
        return '음악학부'
    elif '의류' in name:
        return '의류학전공'
    elif '의사' in name or '소통' in name:
        return '의사소통능력개발센터'
    elif '인권' in name:
        return '인권상담소'
    elif '입학' in name:
        return '입학처'
    elif '장애' in name:
        return '장애학생지원센터'
    elif '재무' in name or '회계' in name:
        return '재무회계팀'
    elif '전기' in name or '전공과' in name:
        return '전기공학과'
    elif '전략' in name or '평가' in name:
        return '전략평가팀'
    elif '정보 통신' in name or '정보통신' in name or '정보팀' in name or '통신' in name:
        return '정보통신팀'
    elif '조형' in name or '조예' in name:
        return '조형예술전공'
    elif '중앙' in name or '기기' in name:
        return '중앙기기센터'
    elif 'IOT' in name or 'iot' in name:
        return '지능IOT융합전공'
    elif '지적' in name or '재산' in name or '지재' in name:
        return '지적재산권전공'
    elif '진로' in name:
        return '진로지원팀'
    elif '창업' in name:
        return '창업지원센터(창업지원팀)'
    elif '취업' in name:
        return '취업지원팀'
    elif '캠퍼스' in name:
        return '캠퍼스타운사업단'
    elif '커뮤' in name:
        return '커뮤니케이션팀'
    elif '컴과' in name or '컴퓨터' in name or '컴터' in name or '컴공' in name:
        return '컴퓨터과학과'
    elif '핀테크' in name:
        return '핀테크전공'
    elif '학사' in name or '운영' in name:
        return '학사운영팀'
    elif '학사' in name or '운영' in name:
        return '학사운영팀'
    elif '복지' in name and '가족' not in name:
        return '학생복지팀'
    elif '상담' in name and '외국인' not in name and '유학생' not in name and '인권' not in name:
        return '학생상담센터'
    elif '생활관' in name:
        return '학생생활관'
    elif '학술' in name:
        return '학술정보지원팀'
    elif '한일' in name or '한문' in name or '한콘' in name:
        return '한일문화콘텐츠과'
    elif '현장' in name or '실습' in name:
        return '현장실습지원센터'
    elif '화공' in name or '신소재' in name or '화신' in name:
        return '화공신소재전공'
    elif '화에' in name or '에너지' in name or '화학' in name and '신소재' not in name:
        return '화학에너지공학전공'
    elif '휴먼' in name or '휴지' in name:
        return '휴먼지능정보공학과'
    elif '교학' in name and '평생' not in name:
        return '교학팀'
    elif '평생' in name:
        return '평생교육원교학팀'
    elif '교원' in name or '인사' in name and '총무' not in name:
        return '교원인사팀'
    elif '총무' in name or '인사' in name:
        return '총무인사팀'
    elif '국제' in name or '국제 학생' in name and '언어' not in name and '문화' not in name:
        return '국제학생지원팀'
    elif '관리' in name and '보건' not in name and '산학' not in name and '스포츠' not in name:
        return '관리팀'
    elif '보건' in name or '건강' in name and '스포츠' not in name:
        return '보건건강관리센터'
    elif '보건' in name or '건강' in name and '스포츠' not in name:
        return '보건건강관리센터'
    elif '산학' in name or '협력' in name and '연구' not in name and '관리' not in name:
        return '산학협력지원팀'
    elif '산학' in name or '연구' in name and '협력' not in name:
        return '산학협력지원팀'
    elif '스포츠' in name or '스건' in name:
        return '스포츠건강관리전공'
    elif '교육' in name and '국어' not in name and '수학' not in name and '영어' not in name and '공학' not in name and '국제' not in name and '기초' not in name and '소프트웨어' not in name:
        return '교육학과'
    elif '국어' in name or '국교' in name:
        return '국어교육과'
    elif '수학' in name or '수교' in name:
        return '수학교육과'
    elif '영어' in name or '영교' in name:
        return '영어교육과'
    elif '공학' in name and '교육' in name or '공학 센터' in name:
        return '공학교육혁신센터'
    elif '국제' in name and '언어' in name:
        return '국제언어문화교육원'
    elif '기초' in name:
        return '기초교육센터'
    elif '소프트' in name:
        return '소프트웨어융합교육센터'
    else:
        return name

def event_to_date(readEvent):
    etd = Eventtodate.objects.filter(event= readEvent)
    resultStr = ''
    for e in etd:
        resultStr += e.event + e.eventdate +'\n'
    return resultStr

def date_to_event(readDate):
    dte = Datetoevent.objects.filter(date= readDate)
    resultStr = ''
    for d in dte:
        resultStr += d.event1 +'\n'
        resultStr += d.event2 +'\n'
        resultStr += d.event3 +'\n'
    return resultStr

def office_info(readOfficeName):
    oi = Officeinfo.objects.filter(officename= readOfficeName)
    resultStr = ''
    for o in oi:
        resultStr += o.officename+' '+o.officetel+' '+o.officelocation+'\n'

    return resultStr


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
            result += "<div style='margin:30px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'> email : " + k[0][16:] + "</span> </div>"
        elif "소속 :" in l:
            result += "<div style='margin:30px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>"
        elif "전화 :" in l:
            result += "<div style='margin:30px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>"
        elif "위치 :" in l:
            result += "<div style='margin:30px 0;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>  <br>"

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
            result += "<div style='margin:30px 10px;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>"
        else:
            result += "<div style='margin:30px 10px;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>"
    return str(''.join(result))
