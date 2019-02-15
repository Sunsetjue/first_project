from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        if not telephone:
            raise ValueError("请传入手机号码！")
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs["is_superuser"] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs["is_superuser"] = True
        kwargs["is_staff"] = True
        return self._create_user(telephone, username, password, **kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    uid = ShortUUIDField(primary_key=True) # 主键
    telephone = models.CharField(max_length=11, unique=True) # 唯一
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    data_joined = models.DateTimeField(auto_now_add=True)

    objects  = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username