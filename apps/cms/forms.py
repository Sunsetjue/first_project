from apps.form_get_error import FormMixin
from django import forms
from .models import News,Course
from apps.news.models import Carousel

class NewsCategoryForm(forms.Form, FormMixin):
    id = forms.IntegerField(error_messages={"required": "请输入正确的id !"})
    name = forms.CharField(max_length=10)

class NewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField(error_messages={"required": "请输入正确的id！"})
    class Meta:
        model = News
        fields = ["title", "describe", "thumbnail", "content"]

        error_messages ={
            "title": {
                "required": "请输入新闻标题",
                "invalid": "请输入正确的标题"
            },
            "describe": {
                "required": "请输入说明",
                "invalid": "请输入正确的简略说明"
            },
            "content": {
                "required": "请输入内容",
                "invalid": "请输入正确的内容"
            }
        }

class EditNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField(error_messages={"required": "请输入正确的id！"})
    pk = forms.IntegerField(error_messages={"required": "请输入正确的id！"})
    class Meta:
        model = News
        fields = ["title", "describe", "thumbnail", "content"]

        error_messages = {
            "title": {
                "required": "请输入新闻标题",
                "invalid": "请输入正确的标题"
            },
            "describe": {
                "required": "请输入说明",
                "invalid": "请输入正确的简略说明"
            },
            "content": {
                "required": "请输入内容",
                "invalid": "请输入正确的内容"
            }
        }


class CarouselForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Carousel
        fields = ["position", "image_url", "link_to"]

class EditorCarouselForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = Carousel
        fields = ["position", "image_url", "link_to"]

class PublicCourseForm(forms.ModelForm, FormMixin):
    teacher_id = forms.IntegerField()
    category_id = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ["teacher", "category"]