from django.shortcuts import render
from Product.models import Product
from .models import Location

# Create your views here.

def LocationView(request,location_id=None):
    # product = Product.object.get(id=product_id)
    # if product.business is not None:
    #     return render(request,'Location/Location.html',{})
    location = Location.objects.get(id=location_id)
    return render(request,'Location/location.html',{'location':location})



def BusinessLocationView(request,location_id=None):
    # product = Product.object.get(id=product_id)
    # if product.business is not None:
    #     return render(request,'Location/Location.html',{})
    location = Location.objects.get(id=location_id)
    return render(request,'Location/location.html',{'location':location})

