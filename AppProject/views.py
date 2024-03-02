from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import datetime, os
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'homepage.html')


def user_login(request):
    if request.method == 'POST':
        userName = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=userName, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff == 0:
                user = Customer.objects.get(name=userName)
                request.session['userId'] = user.cus_id
                request.session['userName'] = user.name
                request.session['userStatus'] = 'customer'
                return render(request, 'homepage.html')
            else:
                emp = Employ.objects.get(name=userName)
                request.session['userId'] = emp.em_id
                request.session['userName'] = emp.name
                request.session['userStatus'] = emp.role
                return render(request, 'homepage.html')
            messages.add_message(request, messages.INFO, "Login success..")
        else:
            messages.error(request, "User Name or Password not correct..!!!")
            data = {'userName': userName}
            return render(request, 'authention/login.html', data)
    else:
        data = {'userName': ''}
        return render(request, 'authention/login.html', data)


def register(request):
    return render(request, 'authention/register.html')


@login_required(login_url='login')
def brandNew(request):
    if not request.user.is_authenticated:
        # ถ้าผู้ใช้ยังไม่ได้เข้าสู่ระบบ ให้เปลี่ยนเส้นทางไปยังหน้า 'userAuthen'
        return redirect('login')
    return render(request, 'crud/brand/brandNew.html')


@login_required(login_url='login')
def brandList(request):
    if not request.user.is_authenticated:
        # ถ้าผู้ใช้ยังไม่ได้เข้าสู่ระบบ ให้เปลี่ยนเส้นทางไปยังหน้า 'userAuthen'
        return redirect('login')
    return render(request, 'crud/brand/brandList.html')


def brandUpdate(request, id):
    return render(request, 'crud/brand/brandUpdate.html')


def brandDelete(request, id):
    return render(request, 'crud/brand/brandDelete.html')


def carNew(request):
    return render(request, 'crud/car/carNew.html')


def carList(request):
    return render(request, 'crud/car/carList.html')


def carUpdate(request, car_id):
    return render(request, 'crud/car/carUpdate.html')


def carDelete(request, car_id):
    return render(request, 'crud/car/carDelete.html')


def customerNew(request):
    return render(request, 'crud/customer/customerNew.html')


def customerList(request):
    return render(request, 'crud/customer/customerList.html')


def customerUpdate(request, cus_id):
    return render(request, 'crud/customer/customerUpdate.html')


def customerDelete(request, cus_id):
    return render(request, 'crud/customer/customerDelete.html')

def employeNew(request):
    if request.method == 'POST':
        form = EmployForm(request.POST)
        if form.is_valid():
            form.save()
            em_id = request.POST['em_id']
            username = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username, email, password)
            user.first_name = username
            user.is_staff = True
            user.save()
            return redirect('employeList')
        else:
            context = {'form': form}
            return render(request, 'crud/employe/employeNew.html', context)
    else:
        form = EmployForm()
        context = {'form': form}
        return render(request, 'crud/employe/employeNew.html', context)


def employeList(request):
    employees = Employ.objects.all().order_by('em_id')
    context = {'employees': employees}
    return render(request, 'crud/employe/employeList.html', context)


def employeUpdate(request, em_id):
    return render(request, 'crud/employe/employeUpdate.html')


def employeDelete(request, em_id):
    return render(request, 'crud/employe/employeDelete.html')
