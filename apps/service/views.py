from django.shortcuts import render

def service_index(request):
    return render(request, "other/service.html")