#!/usr/bin/env python
# encoding: utf-8
'''
@author: hnx
@contact: 568091431@gqq.com
@file: urls.py.py
@time: 2017/9/2 
@desc:
'''


from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentView,VideoPlayView
from django.conf.urls import url


urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    #添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),



]
