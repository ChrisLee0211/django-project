from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourselistView(View):
    def get(self,request):
        all_course = Course.objects.all().order_by('-add_time')
        sort = request.GET.get('sort','')
        hot_course = Course.objects.all().order_by('-click_nums')[:3]

        #全局搜索功能
        search_keywords = request.GET.get('keywords','') 
        if search_keywords:
            all_course = Course.objects.filter(
                Q(name__icontains=search_keywords)|
                Q(desc__icontains=search_keywords)|
                Q(detail__icontains=search_keywords)
                )
        #课程排序
        if sort:
            if sort == 'hot':
                all_course =all_course.order_by('-click_nums')
            elif sort == 'students':
                all_course =all_course.order_by('-students')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course,4,request=request)
        course = p.page(page)
        return render(request,'course-list.html',{
            'all_course':course,
            'sort':sort,
            'hot_course':hot_course
        })

#课程详情页
class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id = int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user = request.user,fav_id = course.id,fav_type = 1):
                has_fav_course = True
            if UserFavorite.objects.filter(user = request.user,fav_id = course.course_org.id,fav_type = 2):
                has_fav_org = True
            

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag = tag)[:2]
        else:
            relate_course = []
        return render(request,'course-detail.html',{
            'course':course,
            'relate_course':relate_course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })


class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id = int(course_id))
        course.students += 1
        course.save()
        #查询用户是否学习过该课程
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_course = UserCourse.objects.filter(course=course)
        user_ids = [row.user.id for row in user_course]
        #查找id是user_id列表中的学生的课程
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        #取出课程所有id
        course_ids = [row.course.id for row in user_course]
        #获取学过该课程的用户还过其他的所有课程
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        all_resource = CourseResource.objects.filter(course=course)
        return render(request,'course-video.html',{
            'course':course,
            'all_resource':all_resource,
            'relate_course':relate_course
            })


class CommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id = int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.all()
        return render(request,'course-comment.html',{
            'course':course,
            'all_resource':all_resource,
            'all_comment':all_comment
            })

class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")

        course_id = request.POST.get('course_id',0)
        course_id = int(course_id)
        comment = request.POST.get('comments','')
        if course_id > 0 and comment:
            course_comment = CourseComments()
            course = Course.objects.get(id = int(course_id))
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}',content_type="application/json")
