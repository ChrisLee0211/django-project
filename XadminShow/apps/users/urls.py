from django.urls import path,include,re_path

from .views import UserInfoView,UpLoadImageView,UpdatePwdView
from .views import SendEmailCodeView,EmailUpdateView,MyCourseView,MyFavOrgView
from .views import MyFavTeacherView,MyFavCourseView,MyMessageView

urlpatterns = [
    path('info/',UserInfoView.as_view(),name = "user_info"),

    #头像上传
    path('image/upload/',UpLoadImageView.as_view(),name = "image_upload"),

    #个人中心修改密码
    path('update/pwd/',UpdatePwdView.as_view(),name = "update_pwd"),

    #发送邮箱验证码修改邮箱
    path('sendemail_code/',SendEmailCodeView.as_view(),name = "sendemail_code"),

    path('update_email/',EmailUpdateView.as_view(),name = "update_email"),

    #我的课程
    path('mycourse/',MyCourseView.as_view(),name = "mycourse"),

    #我收藏的机构
    path('myfav/org/',MyFavOrgView.as_view(),name="myfav_org"),

    #我收藏的讲师
    path('myfav/teacher/',MyFavTeacherView.as_view(),name="myfav_teacher"),

    #我收藏的课程
    path('myfav/course/',MyFavCourseView.as_view(),name="myfav_course"),

    #我的消息
    path('mymessage/',MyMessageView.as_view(),name="mymessage")

]