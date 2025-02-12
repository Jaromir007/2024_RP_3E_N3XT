from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout


# Create your views here.


def home(request):
    template = loader.get_template('views/home.html')
    return HttpResponse(template.render())

def login_view(request):
    template = loader.get_template('views/login.html')
    return HttpResponse(template.render())

def logout_view(request):
    logout(request)
    return redirect('/')