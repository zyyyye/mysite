from django import template
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm


register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return  Comment.objects.filter(content_type = content_type, object_id = obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    data = {}
    data['content_type'] = content_type.model
    data['object_id'] = obj.pk
    data['reply_comment_id'] = 0
    comment_form = CommentForm(initial = data)
    return comment_form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type = content_type, object_id = obj.pk,parent = None)
    return comments.order_by('-comment_time')
