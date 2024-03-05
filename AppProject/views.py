from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import os

from django.urls import reverse

from .forms import *
from .models import *
from django.contrib import messages


# Create your views here.
def chkPermission(request):
    if 'userStatus' in request.session:
        userStatus = request.session['userStatus']
        if userStatus == 'customer':
            messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
            return False
        else:
            return True
    else:
        if Employ.objects.count() != 0:
            messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
            return False
        else:
            return True


def home(request):
    return render(request, 'homepage.html')


def dashboard(request):
    if not chkPermission(request):
        return redirect('homebase')
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def brandNew(request):
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
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


# @login_required(login_url='login')
def carList(request):
    cars = Car.objects.all().order_by('car_id')
    context = {'cars': cars}
    return render(request, 'crud/car/carList.html', context)


def carGrid(request):
    cars = Car.objects.all().order_by('car_id')
    context = {'cars': cars}
    return render(request, 'crud/car/carGrid.html', context)


@login_required(login_url='login')
def carUpdate(request, car_id):
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
    employees = Employ.objects.all().order_by('em_id')
    context = {'employees': employees}
    return render(request, 'crud/employe/employeList.html', context)


@login_required(login_url='login')
def employeUpdate(request, em_id):
    if not chkPermission(request):
        return redirect('homebase')
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
    if not chkPermission(request):
        return redirect('homebase')
    emp = get_object_or_404(Employ, em_id=em_id)
    if request.method == 'POST':
        emp.delete()
        return redirect('employeList')
    else:
        form = EmployForm(instance=emp)
        form.deleteForm()
        context = {'form': form, 'employee': emp}
        return render(request, 'crud/employe/employeDelete.html', context)


@login_required(login_url='login')
def rentalOrder(request, car_id):
    cus = request.session["userId"]
    car_id = get_object_or_404(Car, car_id=car_id)
    if request.method == 'POST':
        ren_start = request.POST.get('start_date')
        ran_end = request.POST.get('end_date')
        request.session['ren_start'] = ren_start
        request.session['ran_end'] = ran_end
        url = reverse('rentalConfirm', args=[car_id.car_id])
        return redirect(url)

    else:
        context = {'cus': cus, 'car': car_id}
        return render(request, 'rent/rentOrder.html', context)


@login_required(login_url='login')
def rentalConfirm(request, car_id):
    userId = request.session["userId"]
    cus = get_object_or_404(Customer, cus_id=userId)
    car = get_object_or_404(Car, car_id=car_id)
    ren_start = request.session.get('ren_start')
    ran_end = request.session.get('ran_end')

    day_start = datetime.strptime(ren_start, "%Y-%m-%d").date()
    day_end = datetime.strptime(ran_end, "%Y-%m-%d").date()

    day = (day_end - day_start).days

    if car.gear == 'manual':
        gear_rate = 300
    else:
        gear_rate = 600

    if car.car_cc == '125':
        cc_rate = 300
    elif car.car_cc == '150':
        cc_rate = 600
    elif car.car_cc == '300':
        cc_rate = 900
    else:
        cc_rate = 1200

    total = day * (gear_rate + cc_rate)

    if request.method == 'POST':
        rental = RentalOrder()
        rental.car_id = car
        rental.cus_id = cus
        rental.ren_start = day_start
        rental.ran_end = day_end
        rental.total = total
        rental.save()
        car.status = 'disibled'
        car.save()
        del request.session['ren_start']
        del request.session['ran_end']
        url = reverse('rentalList')
        return redirect(url)

    context = {'cus': cus, 'car': car, 'ren_start': day_start, 'ran_end': day_end, 'day': day, 'total': total}
    return render(request, 'rent/rentalConfirm.html', context)


@login_required(login_url='login')
def rentalList(request):
    # customer
    userId = request.session["userId"]
    rental = RentalOrder.objects.filter(cus_id=userId).order_by('-ren_start')
    context = {'rentals': rental}
    return render(request, 'rent/rentalList.html', context)


@login_required(login_url='login')
def rentalListAll(request):
    # employee
    rental = RentalOrder.objects.all().order_by('id')
    context = {'rentals': rental}
    return render(request, 'rent/rentalListAll.html', context)


@login_required(login_url='login')
def rentalPayment(request, rent_id):
    rental = get_object_or_404(RentalOrder, id=rent_id)
    if request.method == 'POST':
        form = rentalPaymentForm(rental_id=rent_id, data=request.POST, files=request.FILES)
        if form.is_valid():
            rental.status = 'ชำระเงินแล้ว'
            rental.save()
            form.save()
            return redirect('rentalList')
        else:
            form = rentalPaymentForm(rental_id=rent_id)
            context = {'rental': rental, 'form': form}
            return render(request, 'rent/rentalPayment.html', context)
    else:
        form = rentalPaymentForm()
        context = {'rental': rental, 'form': form}
        return render(request, 'rent/rentalPayment.html', context)


def rentalPaymentConfirm(request, rent_id):
    rental = get_object_or_404(RentalOrder, id=rent_id)
    rental_id = rental.id
    rentalPayment = RentalPayment.objects.filter(rental_id=rental_id)

    if request.method == 'POST':
        rental.status = 'ยืนยันการชำระเงิน'
        rental.save()
        return redirect('rentalListAll')

    context = {'rental': rental, 'rentalPayment': rentalPayment}
    return render(request, 'rent/rentalPaymentConfirm.html', context)
