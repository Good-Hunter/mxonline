#!/usr/bin/env python
# encoding: utf-8
'''
@author: hnx
@contact: 568091431@gqq.com
@file: adminx.py.py
@time: 2017/8/23 
@desc:
'''
import  xadmin
from  xadmin import views

from .models import EmailVerifyRecord,Banner
class BaseSetting(object):
    enable_themes = True  #主题功能开启
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']

class BnnerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']
    model_icon = 'fa fa-address-book-o'


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BnnerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)