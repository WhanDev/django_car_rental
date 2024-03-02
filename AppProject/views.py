from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def login(request):
    return render(request, 'authention/login.html')


