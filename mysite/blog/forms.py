from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Blog, BlogType


class EditBlogForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    title = forms.CharField(max_length=50, required = True)
    blog_type = forms.ChoiceField(required = True)
    content = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(EditBlogForm,self).__init__(*args,**kwargs)

        all_type = BlogType.objects.all()
        all_type_list = []
        for blog_type in all_type:
            all_type_list.append((blog_type,blog_type))

        self.fields['blog_type'].choices = all_type_list
        

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登陆')
        object_id = self.cleaned_data['object_id']
        # try:
        #     model_obj = Blog.objects.get(pk = object_id)
        # except ObjectDoesNotExist:
        #     raise forms.ValidationError('编辑对象不存在')
        return self.cleaned_data
