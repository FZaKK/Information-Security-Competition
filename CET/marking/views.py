from django.shortcuts import render
from django.http import HttpResponse
from manager import db_operation
from django.shortcuts import render
from marking import models as marking_m
from django.db.models import Avg,Max,Min,Count,Sum  #   引入函数
import json

sel_ids = []

def finish(request):
    # print("sel_ids:",sel_ids)
    # print("tea_ids:",request.session['tea_id'])
    # print("exam_id:",request.session['exam_id'])
    # print("stu_id:",request.session['stu_id'])

    if request.method=='POST':
        data=json.loads(request.body)
        # print("formdata:")
        # print(data)
        tea_id = request.session['tea_id']
        exam_id=request.session['exam_id']
        stu_id=request.session['stu_id']

        #更新答题记录
        sum = 0
        for key,value in data.items():
            id=int(key)
            score=int(value)
            sum += score
            # print(id,':',score)
            try:
                temp_record = marking_m.AnswerRecord.objects.get(id=id)
                temp_record.score = score
                temp_record.is_marked = 1
                temp_record.save()
                db_operation.sys_log('答题记录修改成功', db_operation.LOG_OK)
            except:
                db_operation.sys_log('答题记录修改失败', db_operation.LOG_ERR)
        # print("sum:",sum)

        #更新成绩表
        db_operation.marking.insert_ExamScore(exam_id=exam_id,student_id=stu_id,teacher_id=tea_id,
                                              score=sum)

        return HttpResponse("成功")
    else :
        return HttpResponse("仅支持POST方法")


def mark(request):
    # session验证
    phone_id=request.session.get("user_tea")
    # print(phone_id)
    tea_info,state=db_operation.user.select_tea_by_phone(phone_id)
    _tea_id = tea_info.id
    request.session['tea_id'] = _tea_id
    if state!=db_operation.SUCCESS:
        return HttpResponse("用户不存在")

    exam_ids = []
    marking_exam = marking_m.AnswerRecord.objects.values("exam_id").annotate(exam_num = Count("id"))
    # print(marking_exam)
    sel_ids_t = []
    for marking_exams in marking_exam :
        sel_ids_t = marking_m.AnswerRecord.objects.filter(exam_id=marking_exams['exam_id'],is_marked=0)
        if sel_ids_t.exists():
            exam_ids.append(marking_exams['exam_id'])
    # print(exam_ids)
    if len(exam_ids) <1:
        return HttpResponse("符合阅卷标准的考卷数量不够")

    exams = []
    for exam_id_t in exam_ids:
        exam,status = db_operation.exam.select_exam_by_id(exam_id_t)
        exams.append(exam)
    
    if len(exam_ids) == 1:
        return render(request, 'marking/index0.html', {"exam_list":exams})
    
    return render(request, 'marking/index.html', {"exam_list":exams})



def mark_exam(request):
    # print("ex:")
    # print(request.POST['ex'])
    records0 = []
    records1 = []
    sel_ids.clear()
    request.session['exam_id'] = request.POST['ex']
    sel_ids_t = marking_m.AnswerRecord.objects.filter(exam_id=request.POST['ex'],is_marked=0)
    # print(sel_ids_t[0].id)
    request.session['stu_id'] = sel_ids_t[0].student_id.id
    sel_ids_t = sel_ids_t.filter(student_id= sel_ids_t[0].student_id)

    for sel_ids_t0 in sel_ids_t:
        sel_ids.append(sel_ids_t0.id)
    # print(sel_ids)

    for sel_id in sel_ids:
        record,status=db_operation.marking.select_AnswerRecord_by_id(sel_id)
        ques,q_sta = db_operation.exam.select_question_by_id(id=record.question_id.id)
        if ques.type == 0:
            records0.append(record)
        else:
            records1.append(record)

    return render(request, 'marking/mark_exam.html', {"record0_list":records0,"record1_list":records1})
