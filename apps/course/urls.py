from django.urls import path
from . import views

app_name = "course"

urlpatterns = [
    path("index/", views.course_index, name="index"),
    path("<int:course_id>/", views.course_detail, name="detail"),
    path("course_token/", views.course_token, name="course_token"),
    path("paying_course/<int:course_id>/", views.paying_course, name="paying_course")
]