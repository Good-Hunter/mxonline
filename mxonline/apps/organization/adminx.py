#!/usr/bin/env python
# encoding: utf-8
'''
@author: hnx
@contact: 568091431@gqq.com
@file: adminx.py.py
@time: 2017/8/23 
@desc:
'''
from .models import CityDict,CourseOrg,Teacher
import xadmin

class CityDictAdmin(object):
    list_display = ["name","desc","add_time"]
    search_fields = ["name","desc"]
    list_filter = ["name","desc","add_time"]


class CourseOrgAdmin(object):
    list_display = ["name","desc","catgory","click_nums","fav_nums","image","address","city","add_time"]
    search_fields = ["name","desc","catgory","click_nums","fav_nums","image","address","city"]
    list_filter = ["name","desc","catgory","click_nums","fav_nums","image","address","city","add_time"]
    #relfield_style = "fk-ajax"

class TeacherAdmin(object):
    list_display = ["org","name","work_years","work_company","work_position","points","click_nums","fav_nums","add_time"]
    search_fields = ["org","name","work_years","work_company","work_position","points","click_nums","fav_nums"]
    list_filter = ["org","name","work_years","work_company","work_position","points","click_nums","fav_nums","add_time"]

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)