from django.core.management.base import BaseCommand
from apps.cms.models import News,NewsCategory,Course,CourseCategory,CourseTeacher
from apps.news.models import Carousel,Comment
from django.contrib.auth.models import Group, Permission,ContentType

# 自定义django命令 python manage.py ...(命令名称)
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 编辑分组 编辑组（管理后台写的新闻 评论 轮播图）
        edit1_content_type = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Comment),
        ]
        edit1_permission = Permission.objects.filter(content_type__in=edit1_content_type)
        EditGroup1 = Group.objects.create(name="编辑新闻")
        EditGroup1.permissions.set(edit1_permission)
        EditGroup1.save()
        self.stdout.write(self.style.SUCCESS("新闻组创建成功！"))

        edit2_content_type = [
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Carousel),
            ContentType.objects.get_for_model(CourseTeacher),
        ]
        edit2_permission = Permission.objects.filter(content_type__in=edit2_content_type)
        EditGroup2 = Group.objects.create(name="编辑课程轮播图")
        EditGroup2.permissions.set(edit2_permission)
        EditGroup2.save()
        self.stdout.write(self.style.SUCCESS("课程组创建成功！"))

        # 财务组（管理付费订单）

        # 管理员组 管理财务组和编辑组
        admin_permission = edit1_permission.union(edit2_permission)
        AdminGroup = Group.objects.create(name="管理员")
        AdminGroup.permissions.set(admin_permission)
        AdminGroup.save()
        self.stdout.write(self.style.SUCCESS("管理员组创建成功！"))

        self.stdout.write(self.style.SUCCESS("success!"))
        # 每当执行命令initgroup成功后会打印“success”