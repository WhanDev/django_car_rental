from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import os
from .forms import *
from .models import *
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def brandNew(request):
    if request.method == 'POST':
        form = CarBrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brandList')
    else:
        form = CarBrandForm()
        context = {'form': form}
        return render(request, 'crud/brand/brandNew.html', context)


def brandList(request):
    brand = CarBarnd.objects.all().order_by('id')
    context = {'brand': brand}
    return render(request, 'crud/brand/brandList.html', context)


@login_required(login_url='login')
def brandUpdate(request, id):
    brand = get_object_or_404(CarBarnd, id=id)
    form = CarBrandForm(request.POST or None, instance=brand)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('brandList')
        else:
            context = {'form': form}
            return render(request, 'crud/brand/brandUpdate.html', context)
    else:
        context = {'form': form}
        return render(request, 'crud/brand/brandUpdate.html', context)


@login_required(login_url='login')
def brandDelete(request, id):
    brand = get_object_or_404(CarBarnd, id=id)
    form = CarBrandForm(request.POST or None, instance=brand)
    if request.method == 'POST':
        brand.delete()
        return redirect('brandList')
    else:
        form.deleteForm()
        context = {'form': form, 'brand': brand}
        return render(request, 'crud/brand/brandDelete.html', context)


def user_login(request):
    if request.method == 'POST':
        userName = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=userName, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff == 0:
                user = Customer.objects.get(username=userName)
                request.session['userId'] = user.cus_id
                request.session['userName'] = user.username
                request.session['userStatus'] = 'customer'
                return render(request, 'homepage.html')
            else:
                emp = Employ.objects.get(name=userName)
                request.session['userId'] = emp.em_id
                request.session['userName'] = emp.name
                request.session['userStatus'] = emp.role
                return render(request, 'dashboard.html')

            messages.add_message(request, messages.INFO, "Login success..")
        else:
            messages.error(request, "User Name or Password not correct..!!!")
            data = {'userName': userName}
            return render(request, 'authention/login.html', data)
    else:
        data = {'userName': ''}
        return render(request, 'authention/login.html', data)


def user_logout(request):
    if request.session.get('userId'):
        del request.session["userId"]
        del request.session["userName"]
        del request.session["userStatus"]
        logout(request)
        return redirect('homebase')
    else:
        return redirect('login')

@login_required(login_url='login')
def carNew(request):
    if request.method == 'POST':
        form = CarForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกเรียบร้อย')
            return redirect('carList')
        else:
            car = get_object_or_404(Car, car_id=request.POST['car_id'])
            if car:
                messages.add_message(request, messages.WARNING, "รหัสซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'crud/car/carNew.html', context)
    else:
        form = CarForm()
        context = {'form': form}
        return render(request, 'crud/car/carNew.html', context)


@login_required(login_url='login')
def carList(request):
    cars = Car.objects.all().order_by('car_id')
    context = {'cars': cars}
    return render(request, 'crud/car/carList.html', context)


@login_required(login_url='login')
def carUpdate(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)
    picture = car.picture.name
    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if request.method == 'POST':
        if form.is_valid():
            if os.path.exists(picture):
                os.remove(picture)
            form.save()
            return redirect('carList')
        else:
            context = {'form': form}
            return render(request, 'crud/car/carUpdate.html', context)
    else:
        context = {'form': form}
        return render(request, 'crud/car/carUpdate.html', context)

@login_required(login_url='login')
def carDelete(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)
    picture = car.picture.name
    if request.method == 'POST':
        car.delete()
        if os.path.exists(picture):
            os.remove(picture)
        return redirect('carList')
    else:
        form = CarForm(instance=car)
        form.deleteForm()
        context = {'form': form, 'car': car}
        return render(request, 'crud/car/carDelete.html', context)
    return render(request, 'crud/car/carNew.html')


def customerNew(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            confirmPassword = request.POST['conf_password']
            if password == confirmPassword:
                form.save()
                cus_id = request.POST['cus_id']
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                user = User.objects.create_user(username, email, password)
                user.first_name = username
                user.is_staff = False
                user.save()
                messages.add_message(request, messages.WARNING, "REGISTER SUCCESS")
                return redirect('homebase')
            else:
                messages.add_message(request, messages.WARNING, "รหัสผ่านกับรหัสผ่านที่ยืนยันไม่ตรงกัน...")
                context = {'form': form}
                return render(request, 'crud/customer/customerNew.html', context)
        else:
            messages.add_message(request, messages.WARNING, "ป้อนข้อมูลไม่ถูกต้อง ไม่สมบูรณ์...")
            context = {'form': form}
            return render(request, 'crud/customer/customerNew.html', context)
    else:
        form = CustomerForm()
        context = {'form': form}
        return render(request, 'crud/customer/customerNew.html', context)


def customerList(request):
    customers = Customer.objects.all().order_by('cus_id')
    context = {'customers': customers}
    return render(request, 'crud/customer/customerList.html', context)


@login_required(login_url='login')
def customerUpdate(request, cus_id):
    return render(request, 'crud/customer/customerUpdate.html')


@login_required(login_url='login')
def customerDelete(request, cus_id):
    return render(request, 'crud/customer/customerDelete.html')

@login_required(login_url='login')
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


@login_required(login_url='login')
def employeList(request):
    employees = Employ.objects.all().order_by('em_id')
    context = {'employees': employees}
    return render(request, 'crud/employe/employeList.html', context)


@login_required(login_url='login')
def employeUpdate(request, em_id):
    emp = get_object_or_404(Employ, em_id=em_id)
    if request.method == 'POST':
        form = EmployForm(request.POST or None, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employeList')
        else:
            context = {'form': form}
            return render(request, 'crud/employe/employeeUpdate.html', context)
    else:
        form = EmployForm(instance=emp)
        form.updateForm()
        context = {'form': form, }
        return render(request, 'crud/employe/employeUpdate.html', context)


@login_required(login_url='login')
def employeDelete(request, em_id):
    emp = get_object_or_404(Employ, em_id=em_id)
    if request.method == 'POST':
        emp.delete()
        return redirect('employeList')
    else:
        form = EmployForm(instance=emp)
        form.deleteForm()
        context = {'form': form, 'employee': emp}
        return render(request, 'crud/employe/employeDelete.html', context)
