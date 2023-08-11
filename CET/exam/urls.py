from django.contrib import admin
from django.urls import path , re_path
from exam import views

app_name = 'exam'

urlpatterns = [
    re_path(r'^$|index|exam_info',views.exam_info,name='exam_info'),
    path('online/<int:exam_id>',views.exam_detail,name='exam_detail'),
    path('online/submitted',views.exam_submit,name='exam_submitted'),
    # path('online/',views.exam_d,name='exam_detail'),
    # path('online/submit',views.exam_s,name='exam_detail'),
]