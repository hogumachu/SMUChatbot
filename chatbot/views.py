from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import Datetoevent, Eventtodate, Officeinfo
from ML import seq2seq
# Create your views here.

def home(request):
    context = {}
    return render(request, "chathome.html", context)

def get_info(request):
    text = request.GET['data']
    print(text)

    data = select_function(text)
    print(data)
    context = {'data':data}

    return JsonResponse(context)

def select_function(text):
   sentence = seq2seq.generate_text(seq2seq.make_predict_input(text))
   splitSentence = sentence.split(" ")
   returnValue = ""
   if (splitSentence[0] == 'professor'):
       t = text.split(" ")
       for index in range(len(t)):
           if (t[index] == '교수님') or (t[index] == '교수'):
               returnValue = professor(t[index-1], splitSentence[1])
               break
   elif (splitSentence[0] == 'office'):
       returnValue = office_info(splitSentence[1], splitSentence[2])
   return returnValue


def event_to_date(readEvent):
    etd = Eventtodate.objects.filter(event= readEvent)
    #etd = Eventtodate.objects.all()
    resultStr = ''
    for e in etd:
        resultStr += e.event +" "+ e.eventdate +'\n'
    return resultStr

def date_to_event(readDate):
    dte = Datetoevent.objects.filter(date= readDate[0])

    resultStr = ''
    for d in dte:
        resultStr += d.event1 +'\n'
        resultStr += d.event2 +'\n'
        resultStr += d.event3+'\n'
    print("date to event : "+ readDate[0])
    if len(resultStr) < 3:
        return '일정이 없습니다'
    return resultStr

def office_info(readOfficeName, readWhat):
    oi = Officeinfo.objects.filter(officename= readOfficeName)
    resultStr = ''
    for o in oi:
        if readWhat == '연락처':
            resultStr += o.officename + ' ' + o.officetel + '\n'
        elif readWhat == '위치':
            resultStr += o.officename + ' ' + o.officelocation + '\n'
        else:
            resultStr += o.officename + ' ' + o.officetel + ' ' + o.officelocation + '\n'
    return resultStr

def professor(name, readWhat):
    readUrl = "https://www.smu.ac.kr/search/search.do?menu=교수검색&qt=" + name
    url = requests.get(readUrl).text.encode('utf-8')
    soup = BeautifulSoup(url, 'html.parser')

    pkg_list = soup.findAll("ul", "list4 staff")
    p = str(pkg_list).split('\t')
    result = []
    for l in p:
        if readWhat == '이메일':
            if "mailto" in l:
                k = l.split('">')
                result = "email : " + k[0][16:]
                break
        elif readWhat == '연락처':
            if '전화' in l:
                result = l
                break
            #result +=  l
        elif readWhat == '소속':
            if '소속' in l:
                result = l
                break
            #result += l
        elif readWhat == '위치':
            if '위치' in l:
                result = l
                break
            #result += l
    return str(''.join(result))
    #return result

