# coding=utf-8
from django.shortcuts import render_to_response, render
from polls.models import User
from django.http import HttpResponseRedirect
from .forms import LoginForm 
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/polls/') 
            else:
                return HttpResponseRedirect('/')
    else:
        uf = LoginForm()
    return render_to_response('login.html',{'uf':uf})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))