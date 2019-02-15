from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('<int:news_id>/', views.news_detail, name="news_detail"),
    path('page_number/', views.page_number, name="page_number"),
    path('comment/', views.comment, name="comment"),
]