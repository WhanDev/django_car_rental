from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
import datetime, os

# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def login(request):
    return render(request, 'authention/login.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'homepage.html')
