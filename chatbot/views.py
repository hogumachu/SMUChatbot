from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import Datetoevent, Eventtodate, Officeinfo
from konlpy.tag import Mecab
from datetime import date, timedelta

mecab = Mecab()
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
    dict_entity = {
        'date': ['1학기', '2학기', '하계', '동계', '오늘', '내일', '모레', '다음주', '다음 주' '이번학기', '다음 학기', '이번 학기'],
        'proffessor_name': [],
        'major': [],
        'info': ['이메일', '위치', '전공', '연락처', '학과', ],
        'eventinfo': ['기말고사', '학식', '중간고사', '중간', '기말', '방학', '과사', '시험'],
        'purpose': ['날짜', '교수', '사무실', '학사'],
    }

    get_data_list = text
    morpphed_text = mecab.pos(get_data_list)
    tagged_text = ''
    dt = ''
    dt_year = ''
    pattern = dict()
    for index in range(0, len(morpphed_text)):
        if (morpphed_text[index][1] == 'NNBC'):
            if (index - 1 >= 0):
                if (morpphed_text[index - 1][1] == 'SN'):
                    if (morpphed_text[index][0] == '일'):
                        dt += morpphed_text[index - 1][0] + morpphed_text[index][0]
                    elif (morpphed_text[index][0] == '년'):
                        dt_year += morpphed_text[index - 1][0] + morpphed_text[index][0]
                    else:
                        dt += morpphed_text[index - 1][0] + morpphed_text[index][0] + " "
        if (morpphed_text[index][1] in ['NNG', 'MAG', 'NNP', 'NP', 'SL'] and len(morpphed_text[index][0]) > 1):
            if morpphed_text[index][0] == '교수':
                pattern['proffessor_name'] = morpphed_text[index - 1][0]
                tagged_text = morpphed_text[index][0]
                break
            elif morpphed_text[index][0] == '학기':
                feature_value = morpphed_text[index][1]
                tagged_text += feature_value + " " + morpphed_text[index - 1][0] + morpphed_text[index][0] + ' '
            else:
                feature_value = morpphed_text[index][1]
                tagged_text += feature_value + " " + morpphed_text[index][0] + ' '
    if dt != '':
        pattern['date'] = [dt]
    if pattern.get('date') != None:
        pattern['purpose'] = ['날짜']

    for word in tagged_text.split(' '):
        entity = list(filter(lambda key: word in dict_entity[key], list(dict_entity.keys())))
        if (len(entity) > 0):
            pattern[entity[0]] = [word]
    if dt != '':
        pattern['date'] = [dt]
    if pattern.get('date') != None and pattern.get('purpose') == None:
        pattern['purpose'] = ['날짜']

    df = pattern

    if str(df).find('purpose') == -1:
        for text in get_data_list.split(' '):
            ce = convert_event(text)
            co = convert_office(text)
            if len(ce) > 3:
                df['info'] = convert_event(text)
                df['purpose'] = '학사'
                break
            if len(co) > 3 and co != text:
                df['eventinfo'] = convert_office(text)
                df['purpose'] = '사무실'
                break
            if text == '안녕' or text == '반가워' or text == 'ㅎㅇ' or text == '안녕하세요' or text =='반갑습니다':
                return '안녕하세요! 저는 채팅해조 챗봇입니다. 만나서 반가워요'


    for i in df:
        print(i)
        print(df[i])

    # df[key] == 'value' 로 변경하기

    if str(df['purpose']).find('날짜') != -1:
        if str(df).find('eventinfo') != -1:
            return event_to_date(convert_event(df['eventinfo'][0]))
        elif str(df['date']).find('오늘') != -1:
            return date_to_event(str(date.today().strftime('%-m월 %-d일')))
        elif str(df['date']).find('내일') != -1:
            return date_to_event(str((date.today() + timedelta(1)).strftime('%-m월 %-d일')))
        elif str(df['date']).find('모레') != -1:
            return date_to_event(str((date.today() + timedelta(1)).strftime('%-m월 %-d일')))
        elif str(df['date']).find('다음 주') != -1 or str(df['date']).find('다음주') != -1:
            return date_to_event(str((date.today() + timedelta(7)).strftime('%-m월 %-d일')))
        else:
            return date_to_event(df['date'])
    elif str(df['purpose']).find('교수') != -1:
        if len(professor(df['proffessor_name'])) < 10:
            return '교수님 정보가 없습니다'
        else:
            #print(df['proffessor_name'][0] + " 교수님 정보입니다 !")
            return professor(df['proffessor_name'])
    elif str(df['purpose']).find('사무실') != -1:
        print("Here i am")
        return office_info(df['eventinfo'])
    elif str(df['purpose']).find('학사') != -1:
        print("convert_event :  " + convert_event(df['info']))
        print("not convert_event " + (df['info']))
        if len(df['info']) > len(convert_event(df['info'])):
            return event_to_date(df['info'])
        else:
            return event_to_date(convert_event(df['info']))

    else:
        return '무슨 이야기인지 모르겠어요'

def convert_event(eventString):
    year_str = ""
    date_str = ""
    event_str = ""
    if eventString.find('2020') != -1:
        year_str = '2020학년도 '
    elif eventString.find('2021') != -1:
        year_str = '2021학년도'
    elif eventString in ['1학기', '이번 학기']:
        date_str = '제1학기 '
    elif eventString in ['2학기', '다음 학기']:
        date_str = '제2학기 '
    elif eventString in ['중간고사', '중간 고사', '중간']:
        event_str = '중간고사 기간'
    elif eventString in ['기말고사', '기말 고사', '기말']:
        event_str = '기말고사 기간'
    elif eventString.find('학위') != -1:
        event_str = '학위수여식'
    elif eventString.find('전기') != -1:
        date_str = '전기 '
    elif eventString.find('후기') != -1:
        date_str = '후기 '
    elif eventString.find('동계') != -1:
        date_str = '동계 '
    elif eventString.find('하계') != -1:
        date_str = '하계 '
    elif eventString.find('등록') != -1:
        event_str = '등록기간 '
    elif eventString.find('계절') != -1:
        if date_str != '동계 ':
            if year_str == "":
                year_str = '2021학년도 '
                date_str = '하계 '
            else:
                date_str = '하계 '
        elif year_str == "":
            year_str = '2021학년도 '
        event_str = '계절수업'
        return year_str + date_str + event_str
    elif eventString.find('방학') != -1:
        event_str = '방학'
    elif eventString.find('개강') != -1:
        event_str = '개강'
    elif eventString.find('수강') != -1:
        event_str = '수강신청 기간 <재학생>' # 신입생 편입생 그리고 1차 2차 수강 신청도 고려
    elif eventString.find('평가') != -1:
        event_str = '강의평가 기간'
        if date_str == "":
            date_str = '기말 '
        elif date_str == "전기":
            date_str = '중간'
        elif date_str == '후기':
            date_str = '기말'
    elif eventString.find('등록') != -1:
        event_str = '등록기간'
    elif eventString.find('보강') != -1:
        event_str = '보강 및 자율학습 주간'
    elif eventString.find('성적') != -1:
        event_str = '성적확인, 이의신청 및 정정기간'
    elif eventString.find('정정') != -1:
        event_str = '수강신청 정정 및 취소 기간'
    elif eventString.find('장바구니') != -1:
        event_str = '장바구니 수강신청 기간 <재학생>' # 신입생 편입생
    elif eventString.find('개교기념일') != -1:
        return '개교기념일'
    elif eventString.find('입학식') != -1:
        return '입학식(서울)'
    if year_str == "":
        year_str = "2021학년도 "
    if date_str == "":
        date_str = "제1학기 "
    if event_str == "":
        return ""
    return year_str + date_str + event_str

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
    elif '컴과' in name or '컴퓨터' in name or '컴터' in name or '컴공' in name or '컴퓨터과학과' in name:
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
    print("date to event : "+ resultStr[0])
    if len(resultStr) < 3:
        return '일정이 없습니다'
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

#def office(name):
#    readUrl = "https://"+name+".smu.ac.kr/"+name+"/intro/office.do"
#    url = requests.get(readUrl).text.encode('utf-8')
#    soup = BeautifulSoup(url, 'html.parser')

#    pkg_list = soup.findAll("ul", "ul-type01")
#    p = str(pkg_list).split('<li>')
#    result = []
#    for l in p:
#        l = l.replace("</li>", "").replace("</a>", "").replace("</ul>", "").replace("]", "").replace("\t", "").strip()
#        if "ul class" in l:
#            False
#        elif "<" in l:
#            while l.find('<') != -1:
#                l = l.replace(l[l.find('<'):l.find('>') + 1], "")
#            result += "<div style='margin:30px 10px;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>"
#        else:
#            result += "<div style='margin:30px 10px;text-align:left;'><span style='background-color:#F5F6CE;padding:6px 13px;border-radius:8px;'>" + l + "</span> </div>"
#    return str(''.join(result))
