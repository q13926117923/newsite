from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                                error_messages={'required': '评论内容不能为空'})

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
            '''为了接收传进来的user,之后要用Pop从字典里剔除，否则初始化会报错'''
        super().__init__(*args,**kwargs)

    def clean(self):
        #评论对象验证
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class=ContentType.objects.get(model=content_type).model_class()
            """ContentType作为桥梁,用model_class()方法把得到的字符串信息取到为model类型"""
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj

        except Exception as e:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data