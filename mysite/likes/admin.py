from django.contrib import admin
from .models import LikeRecord,LikeCount
# Register your models here.

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'liked_time','content_object')

@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('liked_num','id','content_object')
