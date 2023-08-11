from django.contrib import admin
from django.urls import path , re_path
from marking import views
 
app_name = 'marking'

urlpatterns = [
    re_path(r'^$|index|marking',views.mark,name='mark'),
    path('mark_exam/', views.mark_exam,name='mark_exam'),
    path('mark_exam/finish/', views.finish,name='finish')
]