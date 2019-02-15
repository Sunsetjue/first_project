from django.shortcuts import redirect,reverse
from .forms import LoginForm,RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from utils import restful
from utils.captcha.my_captcha import Captcha
from utils.captcha.smssender import sms_captcha_sender
from io import BytesIO
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth import get_user_model

@require_POST
def login_view(request):
    forms = LoginForm(request.POST)
    if forms.is_valid():
        telephone = forms.cleaned_data.get("telephone")
        password = forms.cleaned_data.get("password")
        remember = forms.cleaned_data.get("remember")
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="账号已经被冻结！")
        else:
            return restful.params_error(message="账号或者密码错误！")
    else:
        errors = forms.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

@require_POST
def register_view(request):
    User = get_user_model()
    forms = RegisterForm(request.POST)
    if forms.is_valid():
        telephone = forms.cleaned_data.get("telephone")
        password = forms.cleaned_data.get("password1")
        username = forms.cleaned_data.get("username")
        user = User.objects.create_user(telephone=telephone,password=password,username=username)
        login(request, user)
        return restful.ok()
    else:
        errors = forms.get_errors()
        return restful.params_error(message=errors)


def img_captcha(request):
    # 得到图形验证码
    text,image = Captcha.gene_code()
    # 把图形验证码放到bytes流中
    place = BytesIO()
    # 放入 告知图片格式
    image.save(place, 'png')
    # 把文件指针放到最前面
    place.seek(0)

    response = HttpResponse(content_type="image/png")
    # 从BytesIO中读取图片并放到httpresponse 上
    response.write(place.read())
    # 告知文件的大小 从指针头读到尾 tell() 告诉指针所在位置
    response["Content-length"] = place.tell()

    cache.set(text.lower(), text.lower(), 5*60)

    return response

def sms_captcha(request):
    telephone = request.GET.get("telephone")
    verification_code = Captcha.gene_text()
    cache.set(telephone, verification_code, 5*60)
    # bl = sms_captcha_sender(telephone=telephone, captcha=verification_code)
    # if bl:
    #     return restful.ok()
    # else:
    #     return restful.params_error(message="验证码发送错误！")
    print(verification_code)
    return restful.ok()

def memcached_test(request):
    cache.set("username", "sunbin1", 60)
    print(cache.get("username"))
    return HttpResponse("success")