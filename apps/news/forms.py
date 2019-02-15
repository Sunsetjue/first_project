from django import forms
from apps.form_get_error import FormMixin

class CommentForm(forms.Form, FormMixin):
    comment = forms.CharField(error_messages={"required": '评论失败！'})
    news_id = forms.IntegerField()