import os

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *


# Create your views here.
def home(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'authention/login.html')


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


def carNew(request):
    if request.method == 'POST':
        form = CarForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            car_id = newForm.car_id
            filepath = newForm.picture.name
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames) - 1]
            newfilename = car_id + ext
            newForm.save()
            car = get_object_or_404(Car, car_id=car_id)
            car.picture.name = '/cars/' + newfilename
            car.save()
            if os.path.exists('static/cars/' + newfilename):
                os.remove('static/cars/' + newfilename)
            os.rename('static/cars/' + filename, 'static/cars/' + newfilename)
        else:
            car = get_object_or_404(Car, car_id=request.POST['car_id'])
            if car:
                messages.add_message(request, messages.WARNING, "รหัสซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'crud/car/carNew.html', context)
            return redirect('carList')
    else:
        form = CarForm()
        context = {'form': form}
        return render(request, 'crud/car/carNew.html', context)


def carList(request):
    cars = Car.objects.all().order_by('car_id')
    context = {'cars': cars}
    return render(request, 'crud/car/carList.html', context)


def carUpdate(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)
    picture = car.picture.name  # รูปสินค้าเดิม
    if request.method == 'POST':
        form = CarForm(request.POST or None, instance=car, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            car_id = newForm.car_id
            print(newForm.picture.name)
            if newForm.picture.name != picture:  # หากเลือกรูปสินค้าใหม่
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = car_id + ext
                product = get_object_or_404(Car, car_id=car_id)
                product.picture.name = '/cars/' + newfilename
                product.save()
                if os.path.exists('static/cars/' + newfilename):
                    os.remove('static/cars/' + newfilename)
                os.rename('static/cars/' + filename, 'static/cars/' + newfilename)
            else:
                newForm.save()
        return redirect('carList')
    else:
        # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
        form = CarForm(instance=car)
        form.updateForm()
        context = {'form': form}
        return render(request, 'crud/car/carUpdate.html',context)



def carDelete(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)
    picture = car.picture.name
    if request.method == 'POST':
        car.delete()
        if os.path.exists('static' + picture):
            os.remove('static' + picture)
        return redirect('carList')
    else:
        form = CarForm(instance=car)
        form.deleteForm()
        context = {'form': form, 'car': car}
        return render(request, 'crud/car/carDelete.html',context)


def customerNew(request):
    return render(request, 'crud/customer/customerNew.html')


def customerList(request):
    return render(request, 'crud/customer/customerList.html')


def customerUpdate(request, cus_id):
    return render(request, 'crud/customer/customerUpdate.html')


def customerDelete(request, cus_id):
    return render(request, 'crud/customer/customerDelete.html')


def employeNew(request):
    return render(request, 'crud/employe/employeNew.html')


def employeList(request):
    return render(request, 'crud/employe/employeList.html')


def employeUpdate(request, em_id):
    return render(request, 'crud/employe/employeUpdate.html')


def employeDelete(request, em_id):
    return render(request, 'crud/employe/employeDelete.html')
