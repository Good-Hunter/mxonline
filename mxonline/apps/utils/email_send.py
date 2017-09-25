#!/usr/bin/env python
# encoding: utf-8
'''
@author: hnx
@contact: 568091431@gqq.com
@file: email_send.py.py
@time: 2017/8/29 
@desc:
'''
from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ""
    chars = '0123456789'+'ABCDEFGHIJKLMNOPQRSTUVWXYZ'+'abcdefghijklmnopqrstuvwxyz'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+= chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type =="update_email":
        code = random_str(4)
    else :
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    #定义邮件内容

    email_title = ''
    email_boby = ''
    if send_type == 'register':
        email_title = u"注册激活连接"
        email_boby = u"请点击下面的连接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_boby,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = u"密码重置连接"
        email_boby = u"请点击下面的连接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title,email_boby,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = u"密码修改连接"
        email_boby = u"你的邮箱验证码为：{0}".format(code)

        send_status = send_mail(email_title,email_boby,EMAIL_FROM,[email])
