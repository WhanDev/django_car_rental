"""
URL configuration for ProjectRentCars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homebase'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    path('brand/new', views.brandNew, name='brandNew'),
    path('brand/', views.brandList, name='brandList'),
    path('brand/update<id>', views.brandUpdate, name='brandUpdate'),
    path('brand/delete<id>', views.brandDelete, name='brandDelete'),
    
    path('car/new', views.carNew, name='carNew'),
    path('car/', views.carList, name='carList'),
    path('car/update<car_id>', views.carUpdate, name='carUpdate'),
    path('car/delete<car_id>', views.carDelete, name='carDelete'),
    
    path('customer/new', views.customerNew, name='customerNew'),
    path('customer/', views.customerList, name='customerList'),
    path('customer/update<cus_id>', views.customerUpdate, name='customerUpdate'),
    path('customer/delete<cus_id>', views.customerDelete, name='customerDelete'),
    
    path('employe/new', views.employeNew, name='employeNew'),
    path('employe/', views.employeList, name='employeList'),
    path('employe/update<em_id>', views.employeUpdate, name='employeUpdate'),
    path('employe/delete<em_id>', views.employeDelete, name='employeDelete'),
]
