from django.shortcuts import redirect
from utils import restful
from functools import wraps
from django.http import Http404

# 编写关于用户是否登陆的装饰器
def project_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message="请登陆！")
            else:
                return redirect("/")
                # 如果通过ajax请求的则返回首页
    return wrapper

def is_superuser_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper