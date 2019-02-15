from django.shortcuts import render,redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.views import View
from django.views.decorators.http import require_POST,require_GET
from django.utils.decorators import method_decorator
from .models import NewsCategory,News,CourseCategory, CourseTeacher, Course
from .forms import NewsCategoryForm,NewsForm,CarouselForm,EditorCarouselForm,EditNewsForm,PublicCourseForm
from utils import restful
import os
from django.conf import settings
import qiniu
from apps.news.models import Carousel
from apps.news.serializers import CarouselSerializers
from apps.project.models import User
from apps.project.decorators import is_superuser_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse

# Create your views here.
def login_view(request):
    return render(request, "cms/login.html")

@staff_member_required(login_url="index")
def index(request):
    return render(request, "cms/index.html")

@method_decorator(permission_required(perm="news.change_news",login_url="/"),name="dispatch")
class NewsList(View):
    def get(self, request):
        # 定义一个得到第几页的参数的名字 i
        page = int(request.GET.get("i", 1))
        start = request.GET.get("start")
        end = request.GET.get("end")
        title = request.GET.get("title")
        category = int(request.GET.get("category",0) or 0)

        categories = NewsCategory.objects.all()
        newses = News.objects.select_related("category", "author").all()

        if start or end:
            if start:
                start_time = datetime.strptime(start, "%Y/%m/%d")
            else:
                start_time = datetime(year=2016, month=8, day=25)
            if end:
                end_time = datetime.strptime(end, "%Y/%m/%d")
            else:
                end_time = datetime.today()
            print(start_time)
            print(end_time)
            newses = newses.filter(timer__range=(make_aware(start_time), make_aware(end_time)))

        if title:
            newses = newses.filter(title__icontains=title)

        if category:
            newses = newses.filter(category=category)

        # 定义一个分页 每页有两个数据
        p = Paginator(newses, 3)
        page_obj = p.page(page)
        context_page = self.get_around_context(paginator=p, page_obj=page_obj)
        context = {
            "categories": categories,
            "newses": page_obj.object_list,
            "page_obj": page_obj,
            'category_pk': category,
            'start': start,
            'ends': end,
            'title': title,
            "url_query": "&" + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category or ''
            })
        }
        print(end)
        context.update(context_page)
        return render(request, "cms/search_news.html", context=context)

    def get_around_context(self, paginator, page_obj, around=2):
        present = page_obj.number
        end = paginator.num_pages
        left_omit = True
        right_omit = True

        if present <= 2 + around:
            left_ranges = range(1, present+1)
            left_omit = False
        else:
            left_ranges = range(present-around, present+1)

        if present >= end - around - 1:
            right_ranges = range(present+1, end+1)
            right_omit = False
        else:
            right_ranges = range(present+1, present+around+1)

        result = {
            "left_ranges": left_ranges,
            "right_ranges":right_ranges,
            "present": present,
            "end": end,
            "left_omit": left_omit,
            "right_omit": right_omit
        }
        return result

@method_decorator(permission_required(perm="news.add_news",login_url="/"),name="dispatch")
class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {'categories': categories}
        return render(request, "cms/write_news.html", context=context)
    def post(self, request):
        forms = NewsForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get("title")
            describe = forms.cleaned_data.get("describe")
            thumbnail = forms.cleaned_data.get("thumbnail")
            content = forms.cleaned_data.get("content")
            category = NewsCategory.objects.get(id=forms.cleaned_data.get("category"))
            News.objects.create(title=title, describe=describe, thumbnail=thumbnail, content=content, category=category, author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=forms.get_errors())

@method_decorator(permission_required(perm="news.change_news",login_url="/"),name="dispatch")
class EditNewsList(View):
    def get(self,request):
        news_id = request.GET.get("news_id")
        news = News.objects.get(id=news_id)
        categories = NewsCategory.objects.all()
        context = {
            "news": news,
            "categories": categories
        }
        return render(request, "cms/write_news.html", context=context)
    def post(self, request):
        forms = EditNewsForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get("title")
            describe = forms.cleaned_data.get("describe")
            thumbnail = forms.cleaned_data.get("thumbnail")
            content = forms.cleaned_data.get("content")
            category = NewsCategory.objects.get(id=forms.cleaned_data.get("category"))
            pk = forms.cleaned_data.get("pk")
            News.objects.filter(id=pk).update(title=title, describe=describe, thumbnail=thumbnail, content=content, category=category)
            return restful.ok()
        else:
            return restful.params_error(message=forms.get_errors())

@permission_required(perm="news.delete_news",login_url="/")
def delete_news(request):
    news_id = request.POST.get("news_id")
    News.objects.filter(id=news_id).delete()
    return restful.ok()

@require_GET
@permission_required(perm="news.add_newscategory",login_url="/")
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {'categories': categories}
    return render(request, "cms/news_category.html", context=context)

@require_POST
@permission_required(perm="news.add_newscategory",login_url="/")
def add_news_category(request):
    name = request.POST.get("name")
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="分类名已存在！")

@require_POST
@permission_required(perm="news.change_newscategory",login_url="/")
def edit_news_category(request):
    forms = NewsCategoryForm(request.POST)
    if forms.is_valid():
        id = forms.cleaned_data.get("id")
        name = forms.cleaned_data.get("name")
        try:
            NewsCategory.objects.filter(id=id).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message="当前的id不存在！")
    else:
        return restful.params_error(message=forms.get_errors())

@require_POST
@permission_required(perm="news.delete_newscategory",login_url="/")
def delete_news_category(request):
    id = request.POST.get("id")
    try:
        NewsCategory.objects.filter(id=id).delete()
        return restful.ok()
    except:
        return restful.params_error(message="当前id不存在！")

@require_POST
def upload_file(request):
    file = request.FILES.get("file")
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name), 'wb') as nf:
        for chunk in file.chunks():
            nf.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})

@require_POST
def qiniu_token(request):
    access_key = settings.UEDITOR_QINIU_ACCESS_KEY
    secret_key = settings.UEDITOR_QINIU_SECRET_KEY
    q = qiniu.Auth(access_key, secret_key)
    bucket = settings.UEDITOR_QINIU_BUCKET_NAME

    token = q.upload_token(bucket)

    return restful.result(data={'token': token})

@require_GET
@permission_required(perm="news.change_carousel",login_url="/")
def carousel_map(request):
    return render(request, "cms/carousel_map.html")

@require_POST
@permission_required(perm="news.add_carousel",login_url="/")
def carousel(request):
    forms = CarouselForm(request.POST)
    if forms.is_valid():
        position = forms.cleaned_data.get("position")
        image_url = forms.cleaned_data.get("image_url")
        link_to = forms.cleaned_data.get("link_to")
        carousel = Carousel.objects.create(position=position, image_url=image_url, link_to=link_to)
        return restful.result(data={"id": carousel.id})
    else:
        return restful.params_error(message=forms.get_errors())

@permission_required(perm="news.add_carousel",login_url="/")
def carousel_detail(request):
    carousel = Carousel.objects.all()
    serializer = CarouselSerializers(carousel, many=True)
    return restful.result(data=serializer.data)

@permission_required(perm="news.delete_carousel",login_url="/")
def delete_carousel(request):
    carousel_id = request.POST.get("carousel_id")
    Carousel.objects.filter(id=carousel_id).delete()
    return restful.ok()

@permission_required(perm="news.add_carousel",login_url="/")
def editor_carousel(request):
    forms = EditorCarouselForm(request.POST)
    if forms.is_valid():
        pk = forms.cleaned_data.get("pk")
        position = forms.cleaned_data.get("position")
        image_url = forms.cleaned_data.get("image_url")
        link_to = forms.cleaned_data.get("link_to")
        Carousel.objects.filter(id=pk).update(position=position, image_url=image_url, link_to=link_to)
        return restful.ok()
    else:
        return restful.params_error(message=forms.get_errors())

@method_decorator(permission_required(perm="course.change_course",login_url="/"),name="dispatch")
class PublicCourse(View):
    def get(self, request):
        teachers = CourseTeacher.objects.all()
        categories = CourseCategory.objects.all()
        context = {"teachers": teachers, "categories": categories}
        return render(request, "cms/public_course.html", context=context)
    def post(self, request):
        forms = PublicCourseForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get("title")
            category = CourseCategory.objects.get(id=forms.cleaned_data.get("category_id"))
            teacher = CourseTeacher.objects.get(id=forms.cleaned_data.get("teacher_id"))
            video_url = forms.cleaned_data.get("video_url")
            picture_url = forms.cleaned_data.get("picture_url")
            price = forms.cleaned_data.get("price")
            course_time = forms.cleaned_data.get("course_time")
            introduction = forms.cleaned_data.get("introduction")
            Course.objects.create(title=title, category=category, teacher=teacher, video_url=video_url, picture_url=picture_url, price=price, course_time=course_time, introduction=introduction)
            return restful.ok()
        else:
            return restful.params_error(message=forms.get_errors())

@is_superuser_required
def staff_index(request):
    staffs = User.objects.filter(is_staff=True)
    context = {"staffs": staffs}
    return render(request, "cms/staff.html", context=context)

@method_decorator(is_superuser_required, name="dispatch")
class AddView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {"groups": groups}
        return render(request, "cms/add_staff.html", context=context)
    def post(self, request):
        telephone = request.POST.get("telephone")
        username = request.POST.get("username")
        try:
            user = User.objects.get(telephone=telephone, username=username)
        except:
            return redirect(reverse("cms:add_staff"))
        user.is_staff = True
        groups_id = request.POST.getlist("groups")
        groups = Group.objects.filter(pk__in=groups_id)
        user.groups.set(groups)
        user.save()
        return redirect(reverse("cms:staff_index"))