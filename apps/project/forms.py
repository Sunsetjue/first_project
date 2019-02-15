from django import forms
from apps.form_get_error import FormMixin
from django.core import validators
from django.core.cache import cache
from .models import User

class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=16, min_length=6, error_messages={"max_length": '请输入小于10位的密码！',
                                                                            "min_length": '请输入大于6位的密码！',
                                                                            "required": '请输入正确的密码！'
                                                                            })
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form, FormMixin):
    password1 = forms.CharField(max_length=16, min_length=6, error_messages={"max_length": '请输入小于10位的密码！',
                                                                            "min_length": '请输入大于6位的密码！',
                                                                            "required": '请输入正确的密码！'
                                                                            })

    password2 = forms.CharField(max_length=16, min_length=6, error_messages={"max_length": '请输入小于10位的密码！',
                                                                            "min_length": '请输入大于6位的密码！',
                                                                            "required": '请输入正确的密码！'
                                                                            })
    #telephone = forms.CharField(validators=[validators.RegexValidator(r"1[345678]/d{9}", message="请输入正确的电话号码！")])
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=10)
    img_captcha = forms.CharField(max_length=4, min_length=4)
    sms_captcha = forms.CharField(max_length=4, min_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        telephone = cleaned_data.get("telephone")
        if password1 != password2:
            raise forms.ValidationError("两次密码输入不一致！")

        img_captcha1 = cleaned_data.get("img_captcha")
        sms_captcha1 = cleaned_data.get("sms_captcha")
        img_captcha2 = cache.get(img_captcha1.lower())
        sms_captcha2 = cache.get(telephone)
        if img_captcha2 != img_captcha1.lower() or not img_captcha2:
            raise forms.ValidationError("图形验证码验证错误！")
        if sms_captcha2.lower() != sms_captcha1.lower() or not sms_captcha2:
            raise forms.ValidationError("短信验证码错误！")

        exist = User.objects.filter(telephone=telephone).exists()
        if exist:
            raise forms.ValidationError("该电话号码已经被注册！")

        return cleaned_data