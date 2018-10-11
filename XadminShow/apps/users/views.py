import json

from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from users.models import UserProfile,EmailVerifyRecord
from users.form import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UpLoadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import Teacher,CourseOrg
from course.models import Course
from .models import Banner

# Create your views here.



class CustomBackend(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class ActiveUserView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")
            if UserProfile.objects.filter(email = user_name):
                return render (request,'register.html',{'msg':'用户已存在','register_form':register_form})

            pass_word = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name   #这样注册可以用邮箱也可以用用户名作为账户
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            
            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '注册成功，欢迎加入'
            user_message.save()

            send_register_email(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse('index'))

class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    from django.urls import reverse
                    return HttpResponseRedirect(reverse('index'))
                    #return render(request,'index.html')，之前用render发现一个渲染的问题，一旦登出再登录，页面图片一片空白。
                else:
                    return render(request,'login.html',{'msg':'用户未激活'})
            else:
                return render(request,'login.html',{'msg':'用户或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request,'success_send.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


class ResetView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email    
                return render(request,'password_reset.html',{'email':email})  #传入email在页面里构建一个<input type="hidden" name="email" value="{{email}}">
        else:                                                                 #目的是为了让后面POST的时候能拿到该用户的email，然后根据email在数据库中找到原来的密码进行重置
            return render(request,'active_fail.html')
        return render(request,'login.html')

#用户修改密码
class ModifyPwdView(View):    
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'msg':'密码不一致','email':email})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd2)
            user.save()
            return render(request,'login.html')

        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html',{})

        
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors),content_type="application/json")


class UpLoadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UpLoadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}',content_type="application/json")

#个人中心修改密码
class UpdatePwdView(View):    
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}',content_type="application/json")

        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type="application/json")


#发送邮箱验证码：
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}',content_type="application/json")

        send_register_email(email,"update_email")

        return HttpResponse('{"status":"success"}',content_type="application/json")

class EmailUpdateView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"email":"验证码出错"}',content_type="application/json")


class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_course = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_course':user_course,
        })


class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        fav_org_list = []
        fav_org = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for org in fav_org:
            org_id = org.fav_id
            orgs = CourseOrg.objects.get(id=org_id)
            fav_org_list.append(orgs)
        return render(request,'usercenter-fav-org.html',{
            'fav_org_list':fav_org_list,
        })

class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self,request):
        fav_teacher_list = []
        fav_teacher = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for teacher in fav_teacher:
            teacher_id = teacher.fav_id
            teachers = Teacher.objects.get(id=teacher_id)
            fav_teacher_list.append(teachers)
        return render(request,'usercenter-fav-teacher.html',{
            'fav_teacher_list':fav_teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    def get(self,request):
        fav_course_list = []
        fav_course = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for course in fav_course:
            course_id = course.fav_id
            courses = Course.objects.get(id=course_id)
            fav_course_list.append(courses)
        return render(request,'usercenter-fav-course.html',{
            'fav_course_list':fav_course_list
        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_message = UserMessage.objects.filter(user = request.user.id)

        #用户点击进入个人消息后清空未读消息记录
        all_unread_message = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for row in all_unread_message:
            row.has_read = True
            row.save()

        #对我的消息课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message,4,request=request)
        message = p.page(page)
        return render(request,'usercenter-message.html',{
            'message':message
        })

#首页配置
class IndexView(View):
    def get(self,request):
        #取出轮播图,并且根据index数值排序
        all_banner = Banner.objects.all().order_by('index')
        #取出course中的轮播图
        banner_course = Course.objects.filter(is_banner=True)[:2]
        #取出课程
        course = Course.objects.filter(is_banner=False)[:6]
        #取出所有机构
        all_org = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banner':all_banner,
            'banner_course':banner_course,
            'course':course,
            'all_org':all_org
        })

def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response