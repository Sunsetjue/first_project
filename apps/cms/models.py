from django.db import models

# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=10)

class News(models.Model):
    title = models.CharField(max_length=50)
    thumbnail = models.URLField()
    describe = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey('NewsCategory', on_delete=models.SET_NULL, null=True)
    timer = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('project.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-timer"]

class CourseCategory(models.Model):
    name = models.CharField(max_length=30)

class CourseTeacher(models.Model):
    name = models.CharField(max_length=4)
    name_title = models.CharField(max_length=50)
    profile = models.CharField(max_length=1000)

class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey("CourseCategory", on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey("CourseTeacher", on_delete=models.DO_NOTHING) # do_noting 是指外键被删除了 这个数据不做任何处理
    video_url = models.URLField()
    picture_url = models.URLField()
    price = models.FloatField()
    course_time = models.IntegerField()
    introduction = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)