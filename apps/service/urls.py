from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
    path('index/', views.service_index, name="index")
]