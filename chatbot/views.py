from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import Datetoevent, Eventtodate, Officeinfo
from ML import seq2seq
from datetime import date
import datetime
from konlpy.tag import Mecab
mecab = Mecab()

# 웹 생성
def home(request):
    context = {}
    return render(request, "chathome.html", context)

# 웹에서 입력 받은 text 받고 전달
def get_info(request):
    text = request.GET['data']
    print("##### get_info - text : " +text)
    data = select_function(text)
    context = {'data' : data}
    print(data)
    return JsonResponse(context)

# seq2seq로 text를 보내 의도 파악을 하고 그에 해당하는 function (def) 으로 text를 보내 그에 대한 응답 text를 리턴
def select_function(text):
   sentence = seq2seq.generate_text(seq2seq.make_predict_input(text))
   print("##### select_function - seq2seq : " + sentence)
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
   elif (splitSentence[0] == 'cafeteria'):
       returnValue = cafeteria(splitSentence[1])
   elif (splitSentence[0] == 'event'):
       returnValue = event_to_date(splitSentence[1], splitSentence[2], splitSentence[3:])
   elif (splitSentence[0] == 'date'):
       returnValue = date_to_event(text)
   return returnValue

# 이벤트 (학사에 대한 내용) 으로 그 이벤트의 날짜를 알 수 있음
def event_to_date(year, semester, event):
    # ex) 중간고사, 2021년, 2학기
    if year == "now":
        year = "2021년"
    if semester == "now":
        semester = "1학기"
    addEvent = ""
    for i in event:
        addEvent += i+ " "
    addEvent = addEvent[:-2]
    readEvent = year + " " + semester + " " + addEvent
    print("##### event_to_date - year + semester + event : " + readEvent)

    if (addEvent == "입학"):
        etd = Eventtodate.objects.filter(event= "입학식")
    elif (addEvent == "개교기념일"):
        etd = Eventtodate.objects.filter(event="개교기념일")
    elif (readEvent == "2021년 2학기 기말고사 기간"):
        etd = Eventtodate.objects.filter(event="2021년 2학기 기말고사")
    else:
        etd = Eventtodate.objects.filter(event=readEvent)
    resultStr = []
    for e in etd:
        resultStr += [e.event + " " + e.eventdate1]
        if (e.eventdate2 != None):
            resultStr +=  [e.eventdate2]
        if (e.eventdate3 != None):
            resultStr +=  [e.eventdate3]
    return resultStr

# 날짜로 그 날짜에 어떤 이벤트가 있는지 알 수 있음
def date_to_event(text):
    get_data_list = text

    morpphed_text = mecab.pos(get_data_list)
    result = []
    readDate = ""
    for i in morpphed_text:
        if i[1] == "SN":
            result += [i[0]]
    if (len(result) == 3):
        readDate = result[1] + "월" + " " + result[2] + "일"
    elif (len(result) == 2):
        readDate = result[0] + "월" + " " + result[1] + "일"
    if len(readDate) < 1:
        return ["알 수 없습니다"]
    print("##### date_to_event - date : " + readDate)
    dte = Datetoevent.objects.filter(date= readDate)
    resultStr = []
    for d in dte:
        resultStr += [d.event1]
        resultStr += [d.event2]
        resultStr += [d.event3]
    if len(resultStr) < 3:
        return '일정이 없습니다'
    return resultStr

# office의 이름과 그 office에 대해 알고 싶은 것 (연락처, 위치 등) 을 받아 해당하는 정보를 알 수 있음
def office_info(readOfficeName, readWhat):
    print("##### office_info - officeName, what : " + readOfficeName + " " +readWhat)
    oi = Officeinfo.objects.filter(officename= readOfficeName)
    resultStr = []
    for o in oi:
        if readWhat == '연락처':
            resultStr += [o.officename + ' ' + o.officetel]
        elif readWhat == '위치':
            resultStr += [o.officename + ' ' + o.officelocation]
        else:
            resultStr += [o.officename + ' ' + o.officetel + ' ' + o.officelocation]
    return resultStr

# 교수님 성함과 교수님에 대해 알고 싶은 것 (연락처, 이메일, 전공 등) 을 받아 해당하는 정보를 알 수 있음
def professor(name, readWhat):
    print("##### professor - name, what : " + name + " " + readWhat)
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
                result += ["email : " + k[0][16:]]
        elif readWhat == '연락처':
            if '전화' in l:
                result += [l]
        elif readWhat == '소속':
            if '소속' in l:
                result += [l]
        elif readWhat == '위치':
            if '위치' in l:
                result += [l]
    #return str(''.join(result))
    return result

# 날짜를 받아 그 날짜에 해당하는 학생식당 메뉴를 알 수 있음 (Only 중식, 현재 석식 진행 안하는 것 같음)
def cafeteria(day):
    readUrl = "https://www.smu.ac.kr/ko/life/restaurantView.do?mode=menuList&srMealCategory=L&srDt=" + str(date.today())
    url = requests.get(readUrl).text.encode('utf-8')
    soup = BeautifulSoup(url, 'html.parser')
    pkg_list = soup.findAll("ul", "s-dot")
    p = str(pkg_list).split('\t')
    food = ["", "", "", "", "", "", "", "", "", "", ""]
    count = 0
    for l in p[5:]:
        a = l.split("\n")
        for k in a:
            if ("ul class=" in k):
                count += 1
            elif ("amp;" in k):
                t = k[4:-5] + "\n"
                t = t.replace("amp;", "")
                food[count] += t
            else:
                food[count] += k[4:-5] + "\n"
    # 1  =  월, 2  =  화, 3  =  수, 4  =  목, 5  =  금
    # 6  =  푸, 7  =  푸, 8  =  푸, 9  =  푸, 10 =  푸
    newDay = day
    def getDay(str):
        if (str == "오늘"):
            dt = date.today()
        elif (str == "내일"):
            dt = date.today() + datetime.timedelta(days=1)
        week = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        day = dt.weekday()
        return week[day]
    if (day == "내일"):
        newDay = getDay("내일")
    elif (day == "오늘"):
        newDay = getDay("오늘")

    print("##### cafeteria - day : " + newDay)

    if (newDay == "월요일"):
        if len(food[1]) > 3:
            return [food[1]]
        else:
            return ["아직 메뉴가 업데이트 되지 않았습니다"]
    elif (newDay == "화요일"):
        if len(food[2]) > 3:
            return [food[2]]
        else:
            return ["아직 메뉴가 업데이트 되지 않았습니다"]
    elif (newDay == "수요일"):
        if len(food[3]) > 3:
            return [food[3]]
        else:
            return ["아직 메뉴가 업데이트 되지 않았습니다"]
    elif (newDay == "목요일"):
        if len(food[4]) > 3:
            return [food[4]]
        else:
            return ["아직 메뉴가 업데이트 되지 않았습니다"]
    elif (newDay == "금요일"):
        if len(food[5]) > 3:
            return [food[5]]
        else:
            return ["아직 메뉴가 업데이트 되지 않았습니다"]
    else:
        return ["알 수 없습니다."]


