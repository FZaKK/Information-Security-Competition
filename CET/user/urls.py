from django.urls import path, re_path
# 从自己的 app 目录引入 views
from user import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

app_name = 'user'
urlpatterns = [
    # 初始界面，选择谁登录

    # 用正则表达式设置，默认界面和index都可以登录
    re_path(r'^$|index', views.index, name='index'),

    path('log', views.log, name='log'),

    path('tea_signin', views.tea_signin, name='tea_signin'),
    path('stu_signin', views.stu_signin, name='stu_signin'),
    path('tea_signup', views.tea_signup, name='tea_signup'),
    path('stu_signup', views.stu_signup, name='stu_signup'),
    path('logout', views.logout, name='logout'),
    path('stu_all', views.stu_all, name='stu_all'),
    path('stu_info', views.stu_info, name='stu_info'),
    path('mod_info_stu', views.mod_info_stu, name='mod_info_stu'),
    path('go_to_exam', views.go_to_exam, name='go_to_exam'),
    path('go_to_mark', views.go_to_mark, name='go_to_mark'),
    path('stu_exam_grade', views.get_stu_exam_grade, name='stu_exam_grade'),
    path('tea_info', views.tea_info, name='tea_info'),
    path('logout_tea', views.logout, name='logout_tea'),
    path('mod_info_tea', views.mod_info_tea, name='mod_info_tea'),
    path('mod_password_stu', views.mod_password_stu, name='mod_password_stu'),
    path('mod_password_tea', views.mod_password_tea, name='mod_password_tea'),
    path('sucess_info', views.sucess_info, name='sucess_info'),
    path('captcha_img/',views.captcha_img,name='captcha_img'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('forget_password_tea',views.forget_password_tea,name='forget_password_tea'),
    path('send',views.send_checkcode,name='send'),
    path('modify',views.modify_pwd, name='modify'),
    path('modify_tea',views.modify_pwd_tea, name='modify_tea'),
    path('introduction',views.introduction, name='introduction'),
    path('English_strategy',views.English_strategy, name='English_strategy'),
    path('testinfo',views.testinfo, name='testinfo'),
    path('testtest',views.testtest, name='testtest'),
    path('test.pdf', serve, {'document_root': settings.MEDIA_ROOT, 'path': 'test.pdf'}, name='test-pdf'),
    path('examiee.pdf', serve, {'document_root': settings.MEDIA_ROOT, 'path': 'examiee.pdf'}, name='test-pdf'),
    path('1.pdf', serve, {'document_root': settings.MEDIA_ROOT, 'path': '1.pdf'}, name='test-pdf'),
    path('2.pdf', serve, {'document_root': settings.MEDIA_ROOT, 'path': '2.pdf'}, name='test-pdf')
]

# 配置静态文件URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)