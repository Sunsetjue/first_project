from django.shortcuts import render
from apps.cms.models import News,NewsCategory
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer,CommentSerializer
from django.http import Http404
from .models import Comment,Carousel
from .forms import CommentForm
from apps.project.decorators import project_login_required
from django.db.models import Q

# Create your views here.
def index(request):
    newses = News.objects.select_related("category", "author").all()[0: settings.PAGE_NUMBER]
    categories = NewsCategory.objects.all()
    carousels = Carousel.objects.all()
    context = {
        "newses": newses,
        "categories": categories,
        "carousels": carousels
    }
    return render(request, 'news/index.html', context=context)

def page_number(request):
    # news/page_number/?l=2
    page = int(request.GET.get("p", 1))
    category_id = int(request.GET.get("category_id", 0))
    start = (page-1)*settings.PAGE_NUMBER
    end = settings.PAGE_NUMBER + start
    if category_id == 0:
        current_news = News.objects.select_related("category", "author").all()[start: end]
    else:
        current_news = News.objects.filter(category__id=category_id)[start: end]
    serializer = NewsSerializer(current_news, many=True)
    data = serializer.data
    return restful.result(data=data)

def news_detail(request, news_id):
    try:
        news = News.objects.select_related("category", "author").prefetch_related("comments__author").get(id=news_id)
        context = {"news": news}
        return render(request, 'news/news_detail.html', context=context)
    except:
        raise Http404

@project_login_required
def comment(request):
    try:
        forms = CommentForm(request.POST)
        if forms.is_valid():
            comment = forms.cleaned_data.get("comment")
            news_id = forms.cleaned_data.get("news_id")
            news = News.objects.get(id=news_id)
            pub_comment = Comment.objects.create(comment=comment, author=request.user, news=news)
            serializer = CommentSerializer(pub_comment)
            return restful.result(data=serializer.data)
        else:
            return restful.params_error(message=forms.get_errors())
    except:
        raise Http404

def search(request):
    p = request.GET.get("p")
    categories = NewsCategory.objects.all()
    carousels = Carousel.objects.all()
    if p:
        newses = News.objects.filter(Q(title__icontains=p)|Q(describe__icontains=p))
    else:
        newses = News.objects.select_related("author", "category").filter(category__name="热点")[0:3]
    context = {
        "newses": newses,
        "categories": categories,
        "carousels": carousels
    }
    return render(request, 'other/search.html', context=context)
