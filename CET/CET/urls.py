"""CET URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path
from django.conf.urls import include
from manager import views as mngr_views
from reg import views as reg_views
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     re_path(r"^$", mngr_views.hello),
#     path('test/', mngr_views.show_items, name='test'),
# ]
urlpatterns = [
    re_path(r"^admin\/?", admin.site.urls),
    re_path(r"^$", mngr_views.hello), # 支持正则表达式

    # 下面为路由分发, 请各个模块按自己的前缀, 在自己的模块内的urls.py编写url路径
    path("manager/", include("manager.urls",namespace="manager")),
    path("exam/", include("exam.urls")),
    path("reg/", include("reg.urls")),
    path("marking/", include("marking.urls")),
    path("user/", include("user.urls")),
]
