from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from . import connect_apiai
from django.db.models import F
from .models import SsuperLecture

def check(keyword):
    queryword = keyword
    lectures = SsuperLecture.objects.filter(lecutrename__contains = queryword)
    db_str = ''
    for lecture in lectures:
        db_str = '과목명 : '+lecture.lecutrename + ' 교수명 : '+lecture.professor + '\n평점 : '+lecture.rate + ' 시험 횟수 : '+lecture.exam + ' 과제량 : '+lecture.homework + ' 학점 비율 : '+lecture.grade + " 조모임 : "+lecture.team + '\n강의평 : '+lecture.text
        #print(lecture.lecutrename, lecture.professor, lecture.rate, lecture.exam, lecture.homework, lecture.grade, lecture.team, lecture.text)

    return db_str


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


@csrf_exempt
def message(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    today_date = datetime.date.today().strftime("%m %d")

    intentName = connect_apiai.get_apiai_intent(content)

    if "1-1. Search - assessment lecture" == intentName:
        apiai_keyword = connect_apiai.get_apiai(content)  # 아마 안될 것 수정해야해
        data_will_be_send = {
            'message':{
                'text' : check(apiai_keyword)

            }

        }

    elif "1-2.Search - Professor" in content:
        data_will_be_send = {
            'message': {
                'text': "hi"
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
