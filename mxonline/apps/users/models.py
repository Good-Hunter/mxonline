# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from  datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name="昵称",default="")
    birday = models.DateField(verbose_name=u"生日",default="1991-1-1")
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default="")
    address = models.CharField(max_length=100,default="")
    mobile = models.CharField(max_length=11,default="")
    image =models.ImageField(upload_to="image/%Y/%m",default="image/default.png",max_length=100)


    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        # 获取用户未读数据数量
        from operation.models import UserMessage  #在使用时才import
        return UserMessage.objects.filter(user=self.id, has_read=False).count()#取出未读消息

    def __unicode__(self):
        return self.username  #from AbstractUser


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改密码")),max_length=20,verbose_name=u"验证码类型")
    send_time = models.DateField(default=datetime.now, verbose_name=u"发送时间")


    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0} ({1})'.format(self.code,self.email)

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m",max_length=100)
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name