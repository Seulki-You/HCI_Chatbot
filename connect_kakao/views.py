from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from . import connect_apiai
from django.db.models import F
from .models import SsuperLecture
import re

def check_lecturename(keyword):
    queryword = keyword
    lectures = SsuperLecture.objects.filter(lecutrename__contains = queryword)
    db_str = ''
    for lecture in lectures:
        db_str = '과목명 : '+lecture.lecutrename + ' 교수명 : '+lecture.professor + '\n평점 : '+lecture.rate + ' 시험 횟수 : '+lecture.exam + ' 과제량 : '+lecture.homework + ' 학점 비율 : '+lecture.grade + " 조모임 : "+lecture.team + '\n강의평 : '+lecture.text
        #print(lecture.lecutrename, lecture.professor, lecture.rate, lecture.exam, lecture.homework, lecture.grade, lecture.team, lecture.text)

    return db_str

def check_professor(keyword):
    queryword = keyword
    professors = SsuperLecture.objects.filter(professor__contains=queryword)
    db_list = []
    for professor in professors:
        db_list.append(professor.lecutrename)
        # print(lecture.lecutrename, lecture.professor, lecture.rate, lecture.exam, lecture.homework, lecture.grade, lecture.team, lecture.text)

    return db_list

def index(request):
    return render(request, 'index.html')


#def db(request):
#    greeting = Greeting()
#    greeting.save()

#    greetings = Greeting.objects.all()

#    return render(request, 'db.html', {'greetings': greetings})


def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })

regex = r'[가-힣]+'
@csrf_exempt
def message(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    today_date = datetime.date.today().strftime("%m %d")

    intentName = connect_apiai.get_apiai_intent(content)

    if "1-1. Search - assessment lecture" == intentName:
        str_lecturename = re.findall(regex, content)
        #apiai_keyword = connect_apiai.get_apiai(content)  # 아마 안될 것 수정해야해
        data_will_be_send = {
            'message':{
                'text' : check_lecturename(''.join(str_lecturename))
            }
        }

    elif "1-2.Search - Professor" in content:
        str_professor = re.findall(regex, content)
        data_will_be_send = {
            'message': {
                'text': str_professor + '교수님 검색 결과입니다.'
            },
            "keybooard" : {
                "type": "buttons",
                "buttons" : check_professor(str_professor)
            }

            # ,
            # 'keyboard': {
            #     'type': 'buttons',
            #     'buttons': ['Choose 1', 'Choose 2']
            # }
        }
    else:
        data_will_be_send = {
            'message': {
                'text': connect_apiai.get_apiai(content)
            }

        }

    return JsonResponse(data_will_be_send)


# 이건이 과연 될 것 인가...
def action(request):
    apiaifulfiilment = request.read().decode('utf-8')
    fulfillment_obj = json.loads(apiaifulfiilment)
    print(fulfillment_obj)

    return
# Create your views here.
