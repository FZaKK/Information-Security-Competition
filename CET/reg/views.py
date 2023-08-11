from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from manager import db_operation as db
from django.contrib import messages
from datetime import datetime, time
from manager import tests
import json
from re import escape
# Create your views here.
def index (request):
    return HttpResponse("<center><h1>reg index </h1></center>")

def template_test(request):
    return render(request, 'reg_template_test.html')
#报考的主界面，直接连接到此界面即可，对于登录信息的检查已有
def reg_main(request):
    info=request.session.get("user_stu")
    if not info:
        return redirect('/user/stu_signin')
    # print(info)
    return render(request, 'reg_main.html')

def ConfirmRegState(request):
    info=request.session.get("user_stu")
    if not info:
        return render(request, 'user/stu_signin')
    stu_info,state=db.user.select_stu_by_phone(info)
    if state==db.NOT_EXIST:
        return HttpResponse("用户不存在")
    # print("stu_id=",stu_info.id)
    information=db.exam2.select_exam_arrangement__not_start_by_stuid(stu_info.id)
    if information[1]==db.NOT_EXIST or information[0]==None or len(information[0])==0:
        # print(information[0])
        # print("full information",stu_info.id,stu_info.name,stu_info.school,stu_info.phone,stu_info.email,stu_info.self_number)
        fullinformation={"身份证号":stu_info.self_number,"姓名":stu_info.name,"学校":stu_info.school,"手机号":stu_info.phone,"邮箱":stu_info.email}
        return render(request, 'checkinformation.html',{'n1':fullinformation})
        #已报名
    elif information[1]==db.SUCCESS:
        #弹出一个对话框，提示已报名
        m={"message":"存在已报名的未结束的考试"}
        return render(request, 'regalerts.html',{'n1':m})
    else:
         m={"message":"错误的查询"}
         return render(request, 'regalerts.html',{'n1':m})

def SelectSite(request):
    #根据session信息获取用户对应的城市，然后查询数据库，返回该城市的考点信息
    info=request.session.get("user_stu")
    if not info:
        return redirect('/user/stu_signin')
    #todo 从数据库中获取全部信息
    fullinformationlist,dbstate=db.exam.select_all_exam()
    fullinformation=[]
    for i in fullinformationlist:
        temp={}
        temp["id"]=i.id
        temp["name"]=i.name
        temp["date"]=i.date.strftime("%Y-%m-%d")
        temp["start_time"]=i.start_time.strftime("%H:%M:%S")
        temp["end_time"]=i.end_time.strftime("%H:%M:%S")
        temp["place"]=i.place
        temp["is_online"]=str(i.is_online)
        temp["max_students"]=str(i.max_students)
        if temp["date"] > datetime.now().strftime("%Y-%m-%d") or (
            temp["date"] == datetime.now().strftime("%Y-%m-%d") and temp["start_time"] > datetime.now().strftime("%H:%M:%S")):
            fullinformation.append(temp)

    # print(fullinformation)
    return render(request, 'SelectSite.html',{'n1':fullinformation})

def TakeAnPosition(request):
    #print("启动")
    info = request.session.get("user_stu")
    if not info:
        return redirect('/user/stu_signin')

    if request.method == 'POST':
        selectedData = request.POST.get('selectedData')  # 获取选中行的索引
        if selectedData:
            # print(selectedData)
            selectedData=json.loads(selectedData)
            #向数据库申请一个考位，并返回申请成功与否，这里不搞这么复杂，直接生成订单
            #向数据库申请创建一个订单，订单状态为未支付，订单号为随机生成的
            id=selectedData["id"]
            # print("exam id is",id)
            stuid,state=db.user.select_stu_by_phone(info)
            if state==db.NOT_EXIST:
                return HttpResponse("用户不存在")
            stuid=stuid.id
            # print("stuid is",stuid)
            #首先看有没有未支付的订单
            orderinfo,state=db.exam.select_ExamOrder_by_stu(stuid)
            if state==db.NOT_EXIST:
                #没有未支付的订单，创建一个新的订单
                # print("create new order")
                db.exam.insert_ExamOder(id,stuid,False,0.01)
                orderinfo,state=db.exam.select_ExamOrder_by_stu(stuid)
                # print("new order id is",orderinfo)
                return render(request, 'reg_main.html')
            elif state==db.SUCCESS:
                for i in orderinfo:
                    if i.paid==False:
                        # print("find an unpaid order")
                        orderinfo=i
                        return render(request, 'reg_main.html')
            print("create new order")
            db.exam.insert_ExamOder(id,stuid,False,0.01)
            orderinfo,state=db.exam.select_ExamOrder_by_stu(stuid)
            print("new order id is",orderinfo)
            return render(request, 'reg_main.html')

def PayOrder(request):
    info=request.session.get("user_stu")
    if not info:
        return HttpResponse("请先登录!")
    if request.method == 'POST':
        order=request.POST.get('selectedData')
        # print("支付的订单是",order)
        if order:
            order=json.loads(order)
            #todo,向数据库申请支付一个订单，订单状态为已支付，订单号为随机生成的
            if(order["是否已付款"]=="True"):
                return HttpResponse("订单已支付！无需再支付")
            else:
                # print(order["订单id"])
                return render(request, 'pay.html',{'n1':order["订单id"]})

        else:
            return HttpResponse("未找到订单或订单已过期！")
    else:
        return HttpResponse("没有找到对应的考点数据！")
    
def CheckOrder(request):
    info=request.session.get("user_stu")
    if not info:
        return redirect('/user/stu_signin')
    #todo 从数据库中获取对应用户的订单信息
    stuid,state=db.user.select_stu_by_phone(info)
    orderinfo,state=db.exam.select_ExamOrder_by_stu(stuid)
    orders=[]
    if orderinfo==None:
        return HttpResponse("未找到订单或订单已过期！")
    for i in orderinfo:
        
        temp={}
        temp["订单id"]=i.id
        temp["考试名称"]=i.exam.name
        temp["考试id"]=i.exam.id
        temp["考生名称"]=i.student.name
        temp["考生id"]=i.student.id
        temp["订单价格"]=i.payment
        temp["支付日期"]=i.pay_time.strftime("%Y-%m-%d")
        temp["是否已付款"]=str(i.paid)
        #对数据处理，防止xss攻击
        for key in temp:
            temp[key]=str(temp[key])
            temp[key]=temp[key].replace("&","&amp;")
            temp[key]=temp[key].replace("<","&lt;")
            temp[key]=temp[key].replace(">","&gt;")
            temp[key]=temp[key].replace("'","&apos;")
            temp[key]=temp[key].replace('"',"&quot;")


            
            

        orders.append(temp)
    # print("全部订单",orders)
    if orders!=[]:
        return render(request, 'checkorder.html', {'n1': orders})
    else:
        return HttpResponse("未找到订单或订单已过期！")
def regalerts(request):
    info=request.session.get("user_stu")
    if not info:
        return redirect('/user/stu_signin')
    return render(request, 'regalerts.html')

def pay(request):
    info=request.session.get("user_stu")
    if not info:
        return redirect('/user/stu_signin')
    order = request.POST.get('order')
    order = json.loads(order)
    # print("order is ",order)
    state=db.exam.pay_ExamOrder(order)
    if state==db.SUCCESS:
        order,state=db.exam.select_ExamOder_by_id(order)
        state=db.exam2.insert_exam_arrangement(order.student.id,order.exam.id)
        # return HttpResponse("支付成功！")
        return render(request, 'payment_success.html')
    else:
        return HttpResponse("支付失败！")