import hashlib
import uuid
import time,datetime

from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from user import models
from user.models import Student
from user.models import Teacher
import random
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from manager import db_operation as db
from .forms import ModifyInfoForm
from .forms import ModifyInfoForm_tea

from .forms import ChangePasswordForm

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from common.captcha_4char import captcha
from io import BytesIO
from django.core.mail import send_mail
import requests
'''
初始页面 表单 http://127.0.0.1:8000/user/index 选择登陆谁
学生登陆界面：http://127.0.0.1:8000/user/stu_signin ，输入用户名和密码，正确的话跳转到下一个用户信息页面，不正确的话保持在该页面，但是不知道为啥错误提示不显示
教师登陆页面：http://127.0.0.1:8000/user/tea_signin ， 同样，可以正确判断输入是否符合，但是报错信息不知道为啥不显示
学生注册：http://127.0.0.1:8000/user/stu_signup，可以判断已存在的用户，密码不一致啥的，还是报错信息不会显示
教师注册：http://127.0.0.1:8000/user/tea_signup，同上
忘记密码的逻辑还没写，不知道忘记密码之后，要靠啥验证身份信息
后边的个人信息页面还没写，明天再写
'''
# 5.24.新问题：注册成功后不会跳转到新页面了

# 作品赛添加引用
import secretflow as sf
import spu


# 新增生成验证码功能

def captcha_img(request):
    img,code=captcha.veri_code()
    # 将code保存到session会话中
    request.session['checkcode']=code
    stream = BytesIO()
    img.save(stream,'PNG')
    return HttpResponse(stream.getvalue())


def index(request):
    return render(request,'users/index.html')


def log(request):
    return render(request, 'log/test.html')



#选择是教师登录还是学生登陆,接收请求数据
@csrf_protect
def choose_sign(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        if login_type == 'student':
            return redirect('user:stu_signin')  # 跳转到学生登录页面的URL名称
            # 跳转过去报错，要设置默认的个人信息吗？
        elif login_type == 'teacher':
            return redirect('user:tea_signin')  # 跳转到教师登录页面的URL名称

    return render(request, 'users/index.html')
#登录

#教师登录

def tea_signin(request):
    if request.method == 'POST':
        id = request.POST.get('account')
        password = request.POST.get('password')
        # 获取表单提交的验证码
        checkcode = request.POST.get('check_code')
        # 获取session会话中的checkcode
        request.session.get('checkcode')
        session_checkcode = request.session.get('checkcode')
        if checkcode and (checkcode.lower() != session_checkcode.lower()):
            # 添加错误信息
            error_message = "验证码填写错误"
            return render(request, 'users/tea_signin.html', {'error_message': '验证码填写错误'})

        tea ,error  = db.user.select_tea_by_phone(id)
        if error == db.NOT_EXIST:
            # 报错信息，用户不存在
            db.sys_log("用户不存在",db.LOG_ERR)
            return render(request,'users/tea_signin.html', {'error_message':'用户不存在'})
        elif tea != None and tea.password == password:
            # 登录成功，跳转到下一个用户信息页面
            db.sys_log("教师登录成功",db.LOG_OK)
            # 会话：记录登陆人
            request.session['user_tea'] = id  # 记录当前用户的身份id
            return redirect('user:tea_info')  # 跳转到用户信息页面的URL名称
        else:
            # 密码错误
            db.sys_log("密码错误",db.LOG_ERR)
            return render(request,'users/tea_signin.html', {'error_message':'密码错误'})

    return render(request,'users/tea_signin.html')


# modified
# here we give a stu dict
stu_dict = {}

#学生登录
def stu_signin(request):
    if request.method == 'POST':
        id = request.POST.get('account')
        password = request.POST.get('password')
        # print(type(id), type(password))
        print(stu_dict)

        # 获取表单提交的验证码
        checkcode=request.POST.get('check_code')
        # 获取session会话中的checkcode
        # request.session.get('checkcode')
        session_checkcode=request.session.get('checkcode')
        if checkcode and (checkcode.lower() != session_checkcode.lower()):
            # 添加错误信息
            error_message = "验证码填写错误"
            return render(request, 'users/stu_signin.html', {'error_message': '验证码填写错误'})

        '''
        stu ,error  = db.user.select_stu_by_phone(id)
        if error == db.NOT_EXIST:
            # 报错信息，用户不存在
            db.sys_log("用户不存在",db.LOG_ERR)
            return render(request,'users/stu_signin.html', {'error_message':'用户不存在'})
        elif stu != None and stu.password == password:
            # 登录成功，跳转到下一个用户信息页面
            db.sys_log("学生登录成功",db.LOG_OK)
            # 会话：记录登陆人
            request.session['user_stu']=id #记录当前用户的身份id
            return redirect('user:stu_all')  # 跳转到用户信息页面的URL名称
        else:
            # 密码错误
            db.sys_log("密码错误",db.LOG_ERR)
            return render(request,'users/stu_signin.html', {'error_message':'密码错误'})
        '''
        if id not in stu_dict:
            # 报错信息，用户不存在
            db.sys_log("用户不存在",db.LOG_ERR)
            return render(request,'users/stu_signin.html', {'error_message':'用户不存在'})
        elif password == stu_dict[id]:
            # 登录成功，跳转到下一个用户信息页面
            db.sys_log("学生登录成功",db.LOG_OK)
            # 会话：记录登陆人
            request.session['user_stu']=id #记录当前用户的身份id
            return redirect('user:stu_all')  # 跳转到用户信息页面的URL名称
        else:
            # 密码错误
            db.sys_log("密码错误",db.LOG_ERR)
            return render(request,'users/stu_signin.html', {'error_message':'密码错误'})
        

    return render(request,'users/stu_signin.html')


#教师注册
def tea_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 检验密码和确认密码是否一致
        if password != confirm_password:
            error_message = '两次输入的密码不一致'
            return render(request, 'users/tea_signup.html', {'error_message': error_message})

        if db.user.insert_tea(username,phone,password)[1] == db.SUCCESS:
            # 注册成功，跳转到用户登录界面
            error_message = None
            # print('数据库添加成功了，下一步应该是重定向到新的界面')
            return redirect('user:tea_signin')  # 跳转到教师登录页面的URL名称

        # 注册失败
        error_message = '注册失败'
        # print('显示注册失败返回到当前页面')
        return render(request, 'users/tea_signup.html', {'error_message': error_message})

    error_message = None
    return render(request, 'users/tea_signup.html')


# 注册成功
def sucess_info(request):
    return render(request, 'users/sucess_info.html')

#学生注册

def stu_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        id_number = request.POST.get('id_number')
        
        # modified, here we need store the phone and password
        stu_dict[phone] = password

        # 检验密码和确认密码是否一致
        if password != confirm_password:
            error_message = '两次输入的密码不一致'
            return render(request, 'users/stu_signup.html', {'error_message': error_message})

        elif db.user.insert_stu(id_number , username,"",password,phone,"")[1] == db.SUCCESS:
            # 注册成功，跳转到用户登录界面
            # print("user.insert_stu是success")
            return redirect('user:stu_signin')  # 跳转到登录页面的URL名称

        else:
            # 注册失败
            # print(len(id_number))
            # print(type(id_number))
            # # 教师添加成功却显示注册失败
            # print("进入了注册失败的逻辑")
            error_message = '注册失败'
            return render(request, 'users/stu_signup.html', {'error_message': error_message})
            # return redirect('stu_signin')  # 跳转到教师登录页面的URL名称
    return render(request, 'users/stu_signup.html')



# 忘记密码
def forget_password(request):
    if request.method == 'POST':
        phone = request.POST.get('account')
        code = request.POST.get('code')
        # print(phone)
        if request.session.get('phone') == code:
            return render(request,'users/modify_pwd.html',{'phone':phone})

    return render(request, 'users/forget_password.html')

def send_checkcode(request):
    phone = request.GET.get('phone')#这里不知道写的对不对
    # 请求第三方网易云信的服务
    # request ---》》当成浏览器
    url='https://api.netease.im/sms/sendcode.action'
    headers = {}
    headers['Content-Type']='application/x-www-form-urlencoded;charset=utf-8'
    headers['AppKey']='d3ba54c3166e3a9a777de9e37d05146d'
    Nonce = str(uuid.uuid4()).replace('-','')
    headers['Nonce']=Nonce
    CurTime = str(int(time.time()))
    headers['CurTime']= CurTime
    AppSecret='403fcd9614f3'

    CheckSum=hashlib.sha1((AppSecret+Nonce+CurTime).encode('utf-8')).hexdigest()
    headers['CheckSum']= CheckSum
    response=requests.post(url=url,data={'mobile':phone},headers=headers)
    # print(response.text)
    json_result = response.json()
    if json_result.get('code')==200:
        request.session['phone']=json_result.get('obj')  #{'15620528620:'7899'}
        return JsonResponse({'msg':'短信发送成功！'})
    else:
        return JsonResponse({'msg':'短信发送失败！'})


#忘记密码 修改密码
def modify_pwd(request):
    pwd = request.POST.get('new_password1')
    # print(pwd)
    # pwd = '123'
    phone = request.POST.get('phone')
    # print(phone)
    # phone='15620524568'
    # 找到user对象
    student = Student.objects.filter(phone=phone).first()
    # new_password = make_password(pwd)
    student.password = pwd
    # print(student.password)
    student.save()
    # print('密码修改成功')
    messages.success(request, '密码修改成功')
    return render(request, 'users/stu_signin.html', {'success_message': '密码修改成功'})


# 忘记密码--教师端

def forget_password_tea(request):
    if request.method == 'POST':
        phone = request.POST.get('account')
        code = request.POST.get('code')
        # print(phone)
        if request.session.get('phone') == code:
            return render(request,'users/modify_pwd_tea.html',{'phone':phone})

    return render(request, 'users/forget_password_tea.html')
# 发送短信的部分仍然使用那个send_checkcode就行

# 忘记密码--修改密码--教师端
def modify_pwd_tea(request):
    pwd = request.POST.get('new_password1')
    # print(pwd)
    # pwd = '123'
    phone = request.POST.get('phone')
    # print(phone)
    # phone='15620524568'
    # 找到user对象
    # student = Student.objects.filter(phone=phone).first()
    teacher = Teacher.objects.filter(phone=phone).first()
    # new_password = make_password(pwd)
    teacher.password = pwd
    # print(teacher.password)
    teacher.save()
    # print('密码修改成功')
    messages.success(request, '密码修改成功')
    return render(request, 'users/tea_signin.html', {'success_message': '密码修改成功'})




# 学生信息界面

# 找到当前活跃的学生
def stu_active(request):
    # return  student instance
    uid = request.session.get('user_stu')
    student_Set = Student.objects.filter(phone=uid)
    if student_Set.count()==0:
        return None
    return student_Set[0]

# 找到当前活跃的老师
def tea_active(request):
    # return  tea instance
    uid = request.session.get('user_tea')
    # print(uid)
    teacher_Set,status = db.user.select_tea_by_phone(uid)
    if teacher_Set and status == db.SUCCESS:
        return teacher_Set
    else:
        return None


# 新的一个界面：学生选择进入哪个子系统
def stu_all(request):

    if request.method == 'POST':

        login_type = request.POST.get('login_type')
        if login_type == '用户中心':
            return redirect('user:stu_info')  # 跳转到学生登录页面的URL名称
            # 跳转过去报错，要设置默认的个人信息吗？
        elif login_type == '考试报名中心':
            return redirect('user:exam_res')  # 跳转到教师登录页面的URL名称
        elif login_type == '线上考试平台':
            return redirect('user:exam_take')
        else:
            return redirect('user:logout')
    # 在当前页面显示学生信息
    user = stu_active(request)
    if not user:
        return redirect('user:stu_signin')
    info = {
        "id" : user.id,
        "self_number" : user.self_number,
        "name": user.name,
        "school": user.school,
        "phone": user.phone,
        "email": user.email,

    }
    context = {"info": info}
    return render(request, 'users/stu_all.html', context)

# 新的一个界面：老师选择进入哪个子系统
def tea_info(request):
    # 在当前页面显示学生信息
    user = tea_active(request)
    if not user:
        return redirect('user:tea_signin')
    info = {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
    }
    context = {"info": info}
    return render(request, 'users/tea_info.html', context)


# def logout(request):
#     return render(request, 'users/logout.html')
# 退出登录
def logout(request):
    # 删除当前cookie
    if request.session.get("user_stu"):
        del request.session["user_stu"]
    return render(request, 'users/logout.html')
# 教师退出登录

def logout_tea(request):
    # 删除当前cookie
    if request.session.get("user_tea"):
        del request.session["user_tea"]
    return render(request, 'users/logout_tea.html')
# 用户中心：进去之后是个人信息界面，左侧有几个选项：一个选项为修改个人信息，可以点击，点击后可以修改除身份证和名字以外的信息，
# 一个选项为修改密码，点击后跳转到修改密码界面
# 一个选项为已报考的考试信息查询（显示一下学生报考的考试名字时间啥的）
# 一个选项为历史考试：点进去有已经考完的试和对应的考试分数
# 需要添加会话，来记录登录人名
def stu_info(request):
    # 在当前页面显示学生信息
    user = stu_active(request)
    if not user:
        return redirect('user:stu_signin')
    info = {
        "id" : user.id,
        "self_number" : user.self_number,
        "name": user.name,
        "school": user.school,
        "phone": user.phone,
        "email": user.email,

    }
    context = {"info": info}
    return render(request, 'users/stu_info.html', context)


# 修改个人信息
def mod_info_stu(request):
    # 获取当前用户的学生信息
    student = stu_active(request)

    if request.method == 'POST':
        form = ModifyInfoForm(request.POST)

        if form.is_valid():
            # 更新学生信息，仅更新非空白字段
            if form.cleaned_data['name']:
                student.name = form.cleaned_data['name']
            if form.cleaned_data['school']:
                student.school = form.cleaned_data['school']
            if form.cleaned_data['phone']:
                student.phone = form.cleaned_data['phone']
            if form.cleaned_data['email']:
                student.email = form.cleaned_data['email']

            student.save()

            return redirect('user:stu_all')  # 重定向到个人信息页面或其他适当的页面

    else:
        form = ModifyInfoForm(initial={
            'name': student.name,
            'school': student.school,
            'phone': student.phone,
            'email': student.email,
        })
        # 移除字段的required属性
        form.fields['name'].required = False
        form.fields['school'].required = False
        form.fields['phone'].required = False
        form.fields['email'].required = False

    return render(request, 'users/mod_info_stu.html', {'form': form, 'student': student})

# 修改个人信息
def mod_info_tea(request):
    # 获取当前用户的学生信息
    teacher = tea_active(request)

    if request.method == 'POST':
        form = ModifyInfoForm_tea(request.POST)

        if form.is_valid() and teacher:
            # 更新学生信息，仅更新非空白字段
            if form.cleaned_data['name']:
                teacher_name = form.cleaned_data['name']
            if form.cleaned_data['phone']:
                teacher_phone = form.cleaned_data['phone']

            db.user.update_tea(teacher.id, teacher_name, teacher_phone,teacher.password)

            return redirect('user:tea_info')  # 重定向到个人信息页面或其他适当的页面

    else:
        form = ModifyInfoForm(initial={
            'name': teacher.name,

            'phone': teacher.phone,

        })
        # 移除字段的required属性
        form.fields['name'].required = False

        form.fields['phone'].required = False


    return render(request, 'users/mod_info_tea.html', {'form': form, 'teacher': teacher})

#修改学生密码

def mod_password_stu(request):
    student = stu_active(request)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            # 验证旧密码是否匹配
            if not student.password == old_password:
                messages.error(request, '旧密码不正确')
                return render(request,'users/mod_password_stu.html', {'error_message':'旧密码不正确'})
                # 验证新密码是否一致
            if new_password1 != new_password2:
                    messages.error(request, '新密码输入不一致')
                    return render(request, 'users/mod_password_stu.html', {'error_message': '新密码输入不一致'})

            # 更新密码
            student.password = form.cleaned_data['new_password1']
            # print(student.password)
            student.save()
            messages.success(request, '密码修改成功')
            return render(request, 'users/stu_signin.html', {'success_message': '密码修改成功'})
    else:
        form = ChangePasswordForm(initial={
                'password':student.password
        })

    return render(request, 'users/mod_password_stu.html',{'form': form})

# 修改老师密码


def mod_password_tea(request):
    teacher = tea_active(request)

    if request.method == 'POST' and teacher:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            # 验证旧密码是否匹配
            if not teacher.password == old_password:

                messages.error(request, '旧密码不正确')
                return render(request,'users/mod_password_tea.html', {'error_message':'旧密码不正确'})
            # 验证新密码是否一致
            if new_password1 != new_password2:
                    messages.error(request, '新密码输入不一致')
                    return render(request, 'users/mod_password_tea.html', {'error_message': '新密码输入不一致'})

            # 更新密码
            teacher_password = form.cleaned_data['new_password1']
            if db.user.update_tea(teacher.id, teacher.name, teacher.phone,teacher_password) == db.SUCCESS:
                messages.success(request, '密码修改成功')
            return render(request, 'users/tea_signin.html', {'success_message': '密码修改成功'})
    else:
        form = ChangePasswordForm(initial={
                'password':teacher.password
        })

    return render(request, 'users/mod_password_tea.html',{'form': form})

# 进入到考试报名中心，另一个

def go_to_exam(request):
    request.session['stu_id'] = db.user.select_stu_by_phone(request.session.get('user_stu'))[0].id
    return HttpResponseRedirect(reverse('exam:exam_info'))

# go to marking for teacher
def go_to_mark(request):
    request.session['tea_id'] = db.user.select_tea_by_phone(request.session.get('user_tea'))[0].id
    return HttpResponseRedirect(reverse('marking:mark'))

def get_stu_exam_grade(request):
    stu = stu_active(request)
    if stu:
        # print(stu.id)
        scores ,err = db.marking.select_all_EScore_by_stu(stu.id)
        if err == db.SUCCESS and scores:
            return render(request, 'users/stu_exam_grade.html', {'scores': scores})
    
    return HttpResponse("You have no exam")

# 新的一个界面：教师选择进入哪个子系统
#教师的子系统分别有：教师个人信息，阅卷系统



# 装饰的界面
def introduction(request):
    return render(request, 'users/introduction.html')
def English_strategy(request):
    return render(request, 'users/English_strategy.html')
def testinfo(request):
    return render(request, 'users/testinfo.html')
def testtest(request):
    return render(request, 'users/test.pdf')