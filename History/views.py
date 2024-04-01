from django.shortcuts import render
from . models import ProductHistory
from Product.models import Product
# Create your views here.


def ProductHistoryDetailView(request,his_id):
    ProdHis = ProductHistory.objects.get(id=his_id)
    return render(request,"History/ProductHistoryDetail.html",{"product":ProdHis})

def ProductEditHistoryView(request,prod_id):
    product = Product.objects.get(id=prod_id)
    allPH = ProductHistory.objects.filter(product=product).order_by("date_updated")
    return render(request,'History/ProductEditHistory.html',{"history":allPH,"product":product})
