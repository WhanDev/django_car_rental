from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def login(request):
    return render(request, 'authention/login.html')

def brandNew(request):
    return render(request, 'crud/brand/brandNew.html')
def brandList(request):
    return render(request, 'crud/brand/brandList.html')
def brandUpdate(request,id):
    return render(request, 'crud/brand/brandUpdate.html')
def brandDelete(request,id):
    return render(request, 'crud/brand/brandDelete.html')

def carNew(request):
    return render(request, 'crud/car/carNew.html')
def carList(request):
    return render(request, 'crud/car/carList.html')
def carUpdate(request,car_id):
    return render(request, 'crud/car/carUpdate.html')
def carDelete(request,car_id):
    return render(request, 'crud/car/carDelete.html')

def customerNew(request):
    return render(request, 'crud/customer/customerNew.html')
def customerList(request):
    return render(request, 'crud/customer/customerList.html')
def customerUpdate(request,cus_id):
    return render(request, 'crud/customer/customerUpdate.html')
def customerDelete(request,cus_id):
    return render(request, 'crud/customer/customerDelete.html')

def employeNew(request):
    return render(request, 'crud/employe/employeNew.html')
def employeList(request):
    return render(request, 'crud/employe/employeList.html')
def employeUpdate(request,em_id):
    return render(request, 'crud/employe/employeUpdate.html')
def employeDelete(request,em_id):
    return render(request, 'crud/employe/employeDelete.html')