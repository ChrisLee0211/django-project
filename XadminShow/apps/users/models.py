from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name = '昵称', default='')
    birthday = models.DateField(verbose_name="生日", null=True, blank = True)
    gender = models.CharField(max_length=8 ,choices=(("male","男"),("female","女")), default="female")
    address = models.CharField(max_length=100,default="")
    mobile = models.CharField(max_length=11,null=True)
    image = models.ImageField(upload_to="image/%Y/%m",default ="image/default.png",max_length=100)

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural = verbose_name

    #重载str方法，否则username显示不出来，因为username是内置在AbstractUser里的字段
    def  __str__(self):
        return self.username

    def get_unread_nums(self):
        #获取用户未读消息的数量
        #放在UserProfile里，是因为它继承了AbstractUser，因此可以在所有页面中调用request对象，需要显示未读消息的数量时，只需要在被继承页面中渲染{{request.get_unread_nums}}
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name="验证码类型",choices=(("register","注册"),("forget","找回密码"),("update_email","修改邮箱")),max_length=20)
    send_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def  __str__(self):
        show_code = self.code
        show_email = self.email
        detailend = '%s(%s)'%(show_code,show_email)
        return detailend

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name="轮播图",max_length=100)
    url = models.URLField(max_length=200,verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def  __str__(self):
        return self.title