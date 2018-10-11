from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.db.models import Q

from .models import CityDict,CourseOrg,Teacher

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .form import UserAskForm
from course.models import CourseOrg,Course
from operation.models import UserFavorite
# Create your views here.

class OrgView(View):
    def get(self,request):
        #机构
        all_org = CourseOrg.objects.all()
        #城市
        all_city = CityDict.objects.all()

        #排名:根据click_nums进行降序排名，拿前三个数据
        hot_orgs = all_org.order_by('-click_nums')[:3]

        #课程机构全局搜索
        search_keywords = request.GET.get('keywords','') 
        if search_keywords:
            all_org = CourseOrg.objects.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))

        #筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            #如果city_id不是空，那么就显示该city_id对应的所有数据
            all_org = all_org.filter(city_id=int(city_id)) #GET请求传回来的不是整数型

        #类别筛选
        category = request.GET.get('ct','')
        if category:
            all_org = all_org.filter(category=category) 

        #排序筛选
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_org =all_org.order_by('-students')
            elif sort == 'courses':
                all_org =all_org.order_by('-course_nums')

         #机构个数
        org_nums = all_org.count()
        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org,4,request=request)
        orgs = p.page(page)
        return render(request,'org-list.html',{
            'all_city':all_city,
            'all_org':orgs,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })

class AddUserAskView(View):
 #用户咨询
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            #注意：JSON字符串，要用双引号"status":"success"，否则ajax接收有问题
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加信息错误"}',content_type="application/json")

#机构首页
class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        #注意，从django1.10之后，is_authenticated()将不再支持，需要将括号去掉
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id = course_org.id,fav_type= 2):
                has_fav = True
        #当我们需要反向查询 A 中某个具体实例所关联的 B 时，用 A.B_set.all()可以查询到，所有外键都可以这样操作
        all_courses =course_org.course_set.all()[:3]
        all_teachers =course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
            
        })

#机构课程
class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id = course_org.id,fav_type= 2):
                has_fav = True
        #当我们需要反向查询 A 中某个具体实例所关联的 B 时，用 A.B_set.all()可以查询到，所有外键都可以这样操作
        all_courses =course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
            
        })

#机构介绍
class OrgDescView(View):
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id = course_org.id,fav_type= 2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
            
        })


#机构讲师
class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id = course_org.id,fav_type= 2):
                has_fav = True
        #当我们需要反向查询 A 中某个具体实例所关联的 B 时，用 A.B_set.all()可以查询到，所有外键都可以这样操作
        all_courses =course_org.course_set.all()
        all_teachers =course_org.teacher_set.all()
        return render(request,'org-detail-teachers.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
            
        })


#用户收藏
class AddFavView(View):
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        #先确认用户是否登录状态:
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")
        #然后查询到底有没有进行过收藏的这条记录：
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id = int(fav_id),fav_type= int(fav_type))
        
        #如果已经存在，那用户再次点击就说明是在进行取消操作，那么就删除数据库里该条记录
        if exist_records:  
            exist_records.delete()
            #在数据库中进行收藏数增减
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            #同时要让本来显示“已收藏”的按钮显示回“收藏”
            return HttpResponse('{"status":"success","msg":"收藏"}',content_type="application/json")
        else:              #如果不存在，那就是想进行收藏，那么就把记录添加到数据库
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}',content_type="application/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}',content_type="application/json")


class TeacherListView(View):
    def get(self,request):
        all_teacher = Teacher.objects.all()
        #课程讲师全局搜索
        search_keywords = request.GET.get('keywords','') 
        if search_keywords:
            all_teacher = Teacher.objects.filter(
                Q(name__icontains=search_keywords)|
                Q(work_company__icontains=search_keywords)|
                Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teacher =all_teacher.order_by('-click_nums')

        sort_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        #对课程讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher,4,request=request)
        teachers = p.page(page)
        return render(request,'teachers-list.html',{
            'all_teacher':teachers,
            'sort':sort,
            'sort_teacher':sort_teacher
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        
        has_teacher_fav = False
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_id = teacher.id,fav_type= 3):
            has_teacher_fav = True
        if UserFavorite.objects.filter(user=request.user,fav_id = teacher.Org.id,fav_type= 2):
            has_org_fav = True

        #讲师排行
        sort_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'sort_teacher':sort_teacher,
            'has_org_fav':has_org_fav,
            'has_teacher_fav':has_teacher_fav
        })