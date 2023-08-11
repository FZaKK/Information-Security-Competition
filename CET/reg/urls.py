from django.contrib import admin
from django.urls import path , re_path
from reg import views

urlpatterns = [
    path("reg_view/", views.index),
    path("reg_template_test/", views.template_test),
    path("reg_main/", views.reg_main,name='reg_main'),
    path('ConfirmRegState/', views.ConfirmRegState, name='ConfirmRegState'),
    path('SelectSite/', views.SelectSite, name='SelectSite'),
    path('TakeAnPosition/', views.TakeAnPosition, name='TakeAnPosition'),
    path('PayOrder/', views.PayOrder, name='PayOrder'),
    path('CheckOrder/', views.CheckOrder, name='CheckOrder'),
    path('regalerts/', views.regalerts, name='regalerts'),
    path('pay/', views.pay, name='pay'),
]