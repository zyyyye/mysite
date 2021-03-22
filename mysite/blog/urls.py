from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/blog/
    path('', views.blog_list, name = "blog_list"),
    path('<int:blog_pk>', views.blog_detail, name = "blog_detail"),
    path('type/<int:blogs_type_pk>', views.blogs_with_type, name = "blogs_with_type"),
    path('date/<int:year>/<int:month>',views.blogs_with_date, name = "blogs_with_date"),
    path('author/<str:author>', views.blogs_with_author, name = "blogs_with_author"),
    path('edit_blogs_list/<str:author>', views.edit_blogs_list, name = 'edit_blogs_list'),
    path('edit_blog/<int:blog_pk>', views.edit_blog, name = 'edit_blog'),
    path('update_blog', views.update_blog, name = 'update_blog'),
    path('create_blog', views.create_blog, name = 'create_blog'),
]