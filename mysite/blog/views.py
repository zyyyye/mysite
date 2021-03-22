from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from read_statistics.utils import read_statistic_once_read
from django.contrib.auth.models import User
from .forms import EditBlogForm
from django.urls import reverse


def get_blog_list_common_data(request,blogs_all_list):
    page_num = request.GET.get('page',1)
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUM)
    page_of_blogs = paginator.get_page(page_num)
    cur_page_num = page_of_blogs.number
    page_range = list(range(max(1,cur_page_num-2),min(cur_page_num+3,paginator.num_pages+1)))
    if page_range[0] > 2:
        page_range.insert(0,'...')
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] < paginator.num_pages-1:
        page_range.append('...')
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year =blog_date.year,
                                        created_time__month = blog_date.month).count
        blog_dates_dict[blog_date] = blog_count


    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['count'] = blogs_all_list.count
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    context['authors'] = User.objects.annotate(blog_count = Count('blog'))
    return context

def blog_list(request):
    blogs_all = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all)
    return render(request, 'blog/blog_list.html',context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    key = read_statistic_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog

    response = render(request, 'blog/blog_detail.html',context)
    response.set_cookie(key, 'true')
    return response

def blogs_with_type(request, blogs_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blogs_type_pk)
    blogs_all = Blog.objects.filter(blog_type = blog_type)
    context = get_blog_list_common_data(request,blogs_all)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs_all = Blog.objects.filter(created_time__year = year,created_time__month = month)
    context = get_blog_list_common_data(request,blogs_all)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render(request, 'blog/blogs_with_date.html', context)

def blogs_with_author(request, author):
    author = User.objects.filter(username = author)[0]
    blogs_all = Blog.objects.filter(author = author)
    context = get_blog_list_common_data(request,blogs_all)
    context['blogs_with_author'] = author
    return render(request, 'blog/blogs_with_author.html', context)

def edit_blogs_list(request, author):
    author = User.objects.filter(username = author)[0]
    blogs_all = Blog.objects.filter(author = author)
    context = get_blog_list_common_data(request,blogs_all)
    context['blogs_with_author'] = author
    return render(request, 'blog/edit_blogs_list.html', context)
    
def edit_blog(request, blog_pk):
    print(request)
    context = {}
    try:
        blog = Blog.objects.get(pk = blog_pk)
    except Blog.DoesNotExist:
        form_data = {
            'object_id' : blog_pk,
        }
    else:
        form_data = {
            'object_id': blog_pk,
            'content' : blog.content,
            'title': blog.title,
            'blog_type': blog.blog_type,
        }
        context['blog'] = blog
    form = EditBlogForm(initial=form_data)
        # form.fields['blog_type'].initial = {str(blog.blog_type):blog.blog_type}
        # form.fields['title'].initial = blog.title

    context['edit_blog_form'] = form
    response = render(request, 'blog/edit_blog.html',context)
    return response

def update_blog(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    edit_blog_form = EditBlogForm(request.POST, user = request.user)
    data = {}
    if edit_blog_form.is_valid():
        blog_id = edit_blog_form.cleaned_data['object_id']     
        try:
            blog = Blog.objects.get(pk = blog_id)
        except Blog.DoesNotExist:
            blog = Blog()
            blog.author = request.user
        blog.title = edit_blog_form.cleaned_data['title'] 
        blog.content = edit_blog_form.cleaned_data['content']
        blog.blog_type = BlogType.objects.filter(type_name = edit_blog_form.cleaned_data['blog_type']).first()
        blog.save()
    else:
        print(edit_blog_form.errors)
    return edit_blogs_list(request, request.user)

def create_blog(request):
    print(request)
    new_id = Blog.objects.first().id + 1
    return edit_blog(request,new_id)

    
