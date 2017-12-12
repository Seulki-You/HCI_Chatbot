from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from . import connect_apiai
from django.db.models import F
from .models import Lecture
import re

def check(request):
    queryword = '정기철'
    lectures = Lecture.objects.filter(professor__contains = queryword)
    db_str = ''
    db_list = []
    for lecture in lectures:
        db_list.append(lecture.lecturename)
        db_str = "'과목명' : "+lecture.lecturename + ", '교수명' : "+lecture.professor + ", '평점' : " + str(lecture.rate) + ", '시험 횟수' : " + lecture.exam + ", '과제량' : " + lecture.homework + ", '학점 비율' : "+lecture.grade + ", '조모임' : "+lecture.team + ", '강의평' : "+lecture.text
        #print(lecture.lecutrename, lecture.professor, lecture.rate, lecture.exam, lecture.homework, lecture.grade, lecture.team, lecture.text)
    print(db_list)
    return HttpResponse(db_list)


def check_lecturename(keyword):
    queryword = keyword
    lectures = Lecture.objects.filter(lecturename__contains = queryword)
    db_str = ''
    db_dict_str = []
    db_list = []
    for lecture in lectures:
        db_list.append('과목명 : '+lecture.lecturename + ', 교수명 : '+lecture.professor)
        db_str = "'과목명' : "+lecture.lecturename + ", '교수명' : "+lecture.professor + ", '평점' : " + lecture.rate + ", '시험 횟수' : " + lecture.exam + ", '과제량' : " + lecture.homework + ", '학점 비율' : "+lecture.grade + ", '조모임' : "+lecture.team + ", '강의평' : "+lecture.text
        db_dict_str.append(db_str)
        #print(lecture.lecturename, lecture.professor, lecture.rate, lecture.exam, lecture.homework, lecture.grade, lecture.team, lecture.text)

    return db_list,db_dict_str

def check_professor(keyword):
    queryword = keyword
    professors = Lecture.objects.filter(professor__contains=queryword)
    db_list = []
    for professor in professors:
        db_list.append(professor.lecturename)
        # print(lecture.lecturename, lecture.professor, lecture.rate, lecture.exam, lecture.homework, lecture.grade, lecture.team, lecture.text)

    #print(db_list)
    return db_list

def index(request):
    return render(request, 'index.html')



def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })

regex = r'[가-힣]+'

use_btn_professor = False
use_btn_lecture=False


@csrf_exempt
def message(request):
    global use_btn_lecture
    global use_btn_professor
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    dict_str = []

    if not use_btn_lecture and not use_btn_professor:
        intentName = connect_apiai.get_apiai_intent(content)

    use_btn_professor = False
    use_btn_lecture = False

    s_professor = ''

    if "1-1. Search - assessment lecture" == intentName:
        str_lecturename = re.findall(regex, content)
        if str_lecturename == '':
            data_will_be_send = {
                'message': {
                    'text': connect_apiai.get_apiai(content)
                },
            }
        elif str_lecturename != str_lecturename.empty:
            list, dict_str = check_lecturename(' '.join(str_lecturename))
            data_will_be_send = {
                'message':{
                    'text' : ' '.join(str_lecturename) + " 과목의 검색 결과입니다. \n원하시는 과목을 선택해주세요."
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons": list,
                }
            }
            use_btn_lecture = True

    elif "1-2.Search - Professor" == intentName:
        str_professor = re.findall(regex, content)
        print(type(str_professor))
        if str_professor == '':
            data_will_be_send = {
                'message': {
                    'text': connect_apiai.get_apiai(content)
                },
            }
        elif str_professor != str_professor.empty:
            data_will_be_send = {
                'message': {
                    'text': str_professor + '교수님 검색 결과입니다. \n원하시는 과목을 선택해주세요.'
                },
                "keybooard": {
                    "type": "buttons",
                    "buttons": check_professor(str_professor)
                }
            }
            use_btn_professor = True
            s_professor = str_professor

    elif use_btn_professor:
        content = 'seach professor'+content   #의미 없는 듯 str을 dict나 list로 변경
        lecture = Lecture.objects.filter(lecturename=content, professor__contain=s_professor)
        str_data = ''
        for data in lecture:
            str_data = "과목명 : " + data.lecturename + ", 교수명 : " + data.professor + ", 평점 : " + data.rate + "\n 시험 횟수 : " + data.exam + ", 과제량 : " + data.homework + ", 학점 비율 : " + data.grade + ", 조모임 : " + data.team + "\n강의평 : " + lecture.text
        data_will_be_send = {
            'message': {
                'text': str_data
            }
        }

    elif use_btn_lecture:
        for data in dict_str:
            dict_load = json.loads(data)
            if '과목명 : '+ dict_load['과목명'] + ', 교수명 : '+dict_load['교수명'] == content:
                data_will_be_send = {
                    'message': {
                        'text': "과목명 : "+dict_load['과목명'] + ", 교수명 : "+dict_load['교수명'] + ", 평점 : " + dict_load['평점'] + "\n시험 횟수 : " + dict_load['시험 횟수'] + ", 과제량 : "+dict_load['과제량'] + ", 학점 비율 : "+dict_load['학점 비율'] + ", 조모임 : "+dict_load['조모임'] + "\n강의평 : "+dict_load['강의평']
                    }
                }
            else:
                data_will_be_send = {
                    'message': {
                        'text': '검색 결과를 찾을 수 없습니다.'
                    }
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
