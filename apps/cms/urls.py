from django.urls import path
from . import views

app_name = "cms"

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('', views.index, name="index"),
    path('news_list/', views.NewsList.as_view(), name="news_list"),
    path('edit_news_list/', views.EditNewsList.as_view(), name="edit_news_list"),
    path('write_news/', views.WriteNewsView.as_view(), name="write_news"),
    path('delete_news/', views.delete_news, name="delete_news"),
    path('news_category/', views.news_category, name="news_category"),
    path('add_news_category/', views.add_news_category, name="add_news_category"),
    path('edit_news_category/', views.edit_news_category, name="edit_news_category"),
    path('delete_news_category/', views.delete_news_category, name="delete_news_category"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('qiniu_token/', views.qiniu_token, name="qiniu_token"),
    path('carousel_map/', views.carousel_map, name="carousel_map"),
    path('carousel/', views.carousel, name="carousel"),
    path('carousel_detail/', views.carousel_detail, name="carousel_detail"),
    path('delete_carousel/', views.delete_carousel, name="delete_carousel"),
    path('editor_carousel/', views.editor_carousel, name="editor_carousel"),
    path('public_course/', views.PublicCourse.as_view(), name="public_course"),
    path('staff_index/', views.staff_index, name="staff_index"),
    path('add_staff/', views.AddView.as_view(), name="add_staff"),
]