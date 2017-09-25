# encoding: utf-8
"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from organization.views import  OrgView
from django.views.static import serve
from mxonline.settings import MEDIA_ROOT
#from users.views import user_login
from users.views import IndexView
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,LogoutView
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #url(r'^$',TemplateView.as_view(template_name="index.html"),name="index"),
    #url(r'^login/$',user_login,name="login"),
    url(r'^$',IndexView.as_view(),name="index"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^logout/$',LogoutView.as_view(),name="logout"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active"),
    url(r'^forget/$',ForgetPwdView.as_view(),name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name="reset_pwd"),
    # 重置密码表单 POST 请求
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    #课程机构的首页
    #url(r'^org_list/$',OrgView.as_view(),name="org_list"),

    #配置上传文件的访问处理函数  处理静态文件
   url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
   #url(r'^static/(?P<path>.*)$',serve,{"document_root":STATIC_ROOT}),

    #课程机构URL配置
    url(r'^org/',include('organization.urls',namespace="org")),

    # 课程列表相关URL配置
    url(r'^course/', include('courses.urls', namespace="courses")),
    url(r'^users/', include('users.urls', namespace="users")),
    #富文本相关URL
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

]
# 全局 404 页面配置（django 会自动调用这个变量）
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'