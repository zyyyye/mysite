from django.urls import path
from . import views

urlpatterns = [
    path('comment',views.update_comment,name = 'comment'),
]