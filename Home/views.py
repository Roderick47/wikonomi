from django.shortcuts import render
from Product.models import Product
import datetime


def HomeView(request):
    products = Product.objects.filter(date_updated__lt=datetime.datetime.now()).order_by('-date_created')
    return render(request,'Home/home.html',{'products':products})

def AboutView(request):
    return render(request,'Home/about.html')
