from django.urls import path,include,re_path
from .views import CourselistView,CourseDetailView,CourseInfoView,CommentView,AddCommentView

urlpatterns = [
    path('list/',CourselistView.as_view(),name = "course_list"),

    re_path(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name = "course_detail"),

    re_path(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name = "course_info"),

    re_path(r'^comment/(?P<course_id>\d+)/$',CommentView.as_view(),name = "course_comment"),
    
    path('add_comment/',AddCommentView.as_view(),name = "add_comment"),
]