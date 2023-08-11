from django.urls import path , re_path
from manager import views

app_name='manager'

urlpatterns = [
    # path对应浏览器url，name是action的对象
    path('', views.ret_manager_index, name='ret_manager_index'),
    path('manage_paper',views.manage_paper, name='manage_paper'),
    path('test/', views.test, name='test'),
    path('test/test_add_item/', views.add_item, name='test_add_item'),
]