import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegisterForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm,ForgetPasswordForm
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html',context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request,user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request = request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)
            user.save()
            del request.session['register_code']
            user = auth.authenticate(username = username, password = password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        register_form = RegisterForm()

    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html',context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def user_info(request):
    context = {}
    #context['user'] = 
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    redirect_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user = request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user = request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(request, 'user/form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request = request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    
    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for','')
    data = {}
    if email != '':
        now = int(time.time())
        send_time = request.session.get('send_time', 0)
        if now - send_time < 30:
            data['status'] = 'ERROR'
        else:
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            request.session[send_for] = code
            request.session['send_code_time'] = now
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                'zyyyye@qq.com',
                [email],
                fail_silently = False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user = request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
    
    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(request, 'user/form.html', context)

def forget_password(request):
    redirect_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST, request = request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email = email)
            user.set_password(new_password)
            user.save()
            del request.session['forget_password_code']
            return redirect(redirect_to)
    else:
        form = ForgetPasswordForm()
    
    context = {}
    context['form'] = form
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['return_back_url'] = redirect_to
    return render(request, 'user/forget_password.html', context)
