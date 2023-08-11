from django.shortcuts import render
from django.http import HttpResponse
from manager import models as manager_m
from manager import db_operation as db
import csv
import os
from django.views.decorators.csrf import csrf_exempt


def hello(request): # 全局的首页
    return render(request, 'index.html')


def ret_manager_index(request): #manager首页
    return render(request, 'manager/index.html')


def add_item(request):  # test func
    if request.method == 'POST':
        name = request.POST.get('name')
        test = request.POST.get('test')
        item = manager_m.TestTable(name=name, test=test)
        item.save()
        # print("Item added successfully")
        return HttpResponse('<script>alert("Item added successfully")</script>')
    else:
        return render(request, 'test.html')


def test(request):  # test function
    items = manager_m.TestTable.objects.all()
    return render(request, 'test.html', {'items': items})


def manage_paper(request): # 添加试卷
    if request.method == "POST":
        req_type = request.POST.get("manage-type")
        if req_type == "gen-paper":
            return gen_paper(request)
        if req_type == "gen-que":
            return upload_que_file(request)
        # return render(request, 'manager/manage_paper.html')
    return render(request, 'manager/manage_paper.html')


def upload_que_file( request): # 仅添加题库
    if request.method == "POST":
        file = request.FILES.get("my-file")
        if file is None:
            return render(request, 'manager/manage_paper.html', {'ret_msg_q': "文件为空"})
        if not file.name.endswith(".csv"):
            return render(request, 'manager/manage_paper.html', {'ret_msg_q': "只能上传 CSV 文件"})
        print("\033[32mupload_que_file:%s\033[0m" % file.name)
        filepath = file.name
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 3:
                        return render(request, 'manager/manage_paper.html', {'ret_msg_q': "文件内容有误, 请确保是否为[int,str,str]格式"})
                    if db.exam.insert_question(int(row[0]), row[1], row[2])[1] == db.SUCCESS:
                        pass
                    else:
                        return render(request, 'manager/manage_paper.html', {'ret_msg_q': "存储失败, 请联系管理员处理"})
        except Exception as e:
            os.remove(filepath)
            return render(request, 'manager/manage_paper.html', {'ret_msg_q': str(e)})
        os.remove(filepath)
        return render(request, 'manager/manage_paper.html', {'ret_msg_q': "文件处理完成"})
    else:
        # return HttpResponse("只支持 POST 请求", status=400)
        return render(request, 'manager/manage_paper.html')


def gen_paper(request): # 添到题库并生成试卷
    '''
    生成一张试卷
    '''
    if request.method == "POST":
        file = request.FILES.get("my-file")
        if file is None:
            # return HttpResponse("文件为空", status=400)
            return render(request, 'manager/manage_paper.html', {'ret_msg_p': "文件为空"})
        if not file.name.endswith(".csv"):
            # return HttpResponse("只能上传 CSV 文件", status=400)
            return render(request, 'manager/manage_paper.html', {'ret_msg_p': "只能上传 CSV 文件"})
        print("\033[32mupload_que_file:%s\033[0m" % file.name)
        filepath = file.name
        que_nums = ''
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 3:
                        return render(request, 'manager/manage_paper.html', {'ret_msg_p': "文件内容有误, 请确保是否为[int,str,str]格式"})
                    q, ok = db.exam.insert_question(int(row[0]), row[1], row[2])
                    if ok == db.SUCCESS:
                        que_nums += str(q.id) if q!= None else "error"
                        que_nums += ","
                    else:
                        return render(request, 'manager/manage_paper.html', {'ret_msg_p': "存储失败, 请联系管理员处理"})
        except Exception as e:
            os.remove(filepath)
            return HttpResponse(str(e), status=400)
        os.remove(filepath)
        p, err = db.exam.insert_paper(que_nums,1)
        info_tobe_ret = "文件处理完成且试卷已添加, 试卷ID:"
        if err == db.SUCCESS:
            info_tobe_ret += str(p.id) if p != None else 'err'
        else:
            info_tobe_ret += "出错, 请联系管理员"
        return render(request, 'manager/manage_paper.html', {'ret_msg_p': info_tobe_ret})
    else:
        # return HttpResponse("只支持 POST 请求", status=400)
        return render(request, 'manager/manage_paper.html')
