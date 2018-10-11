"""XadminShow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from extra_apps import xadmin
from django.views.static import serve
from XadminShow.settings import MEDIA_ROOT

from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,LogoutView,IndexView
from organization.views import OrgView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    path('',IndexView.as_view(), name="index"),
    path('login/',LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('register/',RegisterView.as_view(), name="register"),
    #验证码配置
    path('captcha/', include('captcha.urls')),
    #富文本插件
    re_path(r'^ueditor/',include('DjangoUeditor.urls' )),
    
    re_path(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name = "user_active"),
    path('forget/',ForgetPwdView.as_view(), name="forget_pwd"),
    re_path(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name = "reset_pwd"),
    path('modify_pwd/',ModifyPwdView.as_view(),name="modify_pwd"),
    #课程机构url配置
    #注意！django2.0之后，include的用法有改变，第一个传入的是元组('映射的app的url','app的名字')
    path('org/',include(('organization.urls','organization'),namespace='org')),

    #公开课配置
    path('course/',include(('course.urls','course'),namespace='course')),

    #个人中心配置
    path('users/',include(('users.urls','users'),namespace='users')),
    #配置访问文件的上传处理函数
    re_path(r'^media/(?P<path>.*)/$',serve,{'document_root':MEDIA_ROOT}),

    #re_path(r'^static/(?P<path>.*)/$',serve,{'document_root':STATIC_ROOT})
]

#全局404、500页面
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'