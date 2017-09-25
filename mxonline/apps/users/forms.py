#!/usr/bin/env python
# encoding: utf-8
'''
@author: hnx
@contact: 568091431@gqq.com
@file: forms.py.py
@time: 2017/8/27 
@desc:
'''
from captcha.fields import  CaptchaField
from django import forms

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)#如果传入空值或 None则触发异常
    password = forms.CharField(required=True,min_length=6 )


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(required=True,error_messages={"invalid":u"验证码输入错误"})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True,error_messages={"invalid":u"验证码输入错误"})


class ModifyPwdForm(forms.Form):
    passwprd1 = forms.CharField(required=True,min_length=5)
    passwprd2 = forms.CharField(required=True, min_length=5)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday','address', 'mobile']