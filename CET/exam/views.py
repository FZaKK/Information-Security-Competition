from django.shortcuts import render
from django.http import HttpResponse
from exam import models as exam_m
from manager import db_operation
import json


"""
    在进行考试之前需要有manage对用户登录的凭证(如session等)进行验证，这里是合法性验证后的情况
    * exam_info: 
        判断的对应的用户已经报名的考试信息，如果某一项满足考试要求（如可以参加考试的时间），则有可以
        进行跳转的按钮，进入考试页面。
    
    * exam_detail:
        显示对应的考试试题，支持用户进行答题操作。并且有考试最大作答时间的约束，超时自动提交作答情况。

    * exam_submit:
        对应试者的答题情况进行统计展示，包括每道题作答的答案，整套试卷的作答时间等信息。浏览结束后跳
        转到exam_info对应的界面

"""
def exam_info(request):
    # 模拟session
    # request.session['stu_id']='123456';
    phone_id=request.session.get("user_stu")
    # print(phone_id)
    stu_info,state=db_operation.user.select_stu_by_phone(phone_id)
    if state!=db_operation.SUCCESS:
        return HttpResponse("用户不存在")
    request.session['stu_id']=stu_info.id
    exams,status1=db_operation.exam.select_all_exam_by_stu(stu_info.id)
    exam_arrangement,status2=db_operation.exam2.select_exam_arrangement_by_stuid(stu_info.id)
    # print(exams)
    if (exam_arrangement):
        if status1==db_operation.SUCCESS and status2==db_operation.SUCCESS and exam_arrangement[0]:
            return render(request,'exam/exam_info.html',{'exams':exams,'exam_arrangment':exam_arrangement[0]})
        else :
            return HttpResponse("您未报名考试，或者考试订单未支付")
    else:
        return HttpResponse("您没有报名的考试，请通过报考系统报名后重试！")
    

def exam_detail(request,exam_id):
    # print(exam_id)
    request.session['exam_id']=exam_id
    exam,status=db_operation.exam.select_exam_by_id(exam_id)
    if status!=db_operation.SUCCESS:
        return HttpResponse("在线考试载入错误，请稍后重试！")
    # print(exam)
    # paper,status=db_operation.exam.select_paper_by_id(exam.paper)
    # if status!=db_operation.SUCCESS:
    #     return HttpResponse("在线考试试卷载入错误，请稍后重试！")   
    paper=exam.paper
    # print(paper)
    questions=paper.question_ids
    # questions=questions[1:-1] # 去除首尾的"["、"]"
    items=questions.split(',')
    question_ids=[int(item) for item in items]
    
    question0s,question1s=[],[]
    for question_id in question_ids:
        question_info,status=db_operation.exam.select_question_by_id(question_id)
        if status==db_operation.SUCCESS:
            if question_info.type==0:
                question0s.append([question_id,question_info.question])
            elif question_info.type==1:
                question1s.append([question_id,question_info.question])
    
    if question0s==[] and question1s==[]:
        return HttpResponse("在线考试试卷题目载入错误，请稍后重试！")
    
    return render(request, 'exam/exam_detail.html', {'question0s': question0s, 'question1s': question1s})

def exam_submit(request):
    # exam,status=db_operation.exam.select_exam_by_id()
    # if status!=db_operation.SUCCESS:
    #     return HttpResponse("在线考试信息获取错误，请稍后重试！")
    
    # return render(request,'exam/exam_submitted.html',{'exam':exam,'use_time':use_time})
    if request.method=='POST':
        data=json.loads(request.body)
        exam_id=request.session['exam_id']
        stu_id=request.session['stu_id']
        arrangement,status=db_operation.exam2.select_exam_arrangement_by_stuid(stu_id)
        db_operation.exam2.update_is_commit_ok_by_id(arrangement[0].id)
        for key,value in data.items():
            question_id=int(key)
            stu_answer=value
            # print(key,':',value)
            db_operation.marking.insert_AnswerRecord(exam_id,stu_id,question_id,False,stu_answer)
        return render(request,'exam/exam_submitted.html')
    return HttpResponse("仅支持POST方法")
        















