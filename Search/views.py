from django.shortcuts import render,redirect
from django.db.models import Q
from Product.models import Product
from Business.models import Business
# from .forms import ChooseSpecForm
from .models import pager,combine_query_sets
from django.http import JsonResponse



def SearchView(request):
    query = request.GET.get('q','')
    results_list = Product.objects.filter(
        Q(name__icontains=query)|Q(description__icontains=query)|Q(tags__name__icontains=query)
        )
    results_list = results_list.order_by('price')
    results = pager(request,results_list,3)
    return render(request,'Search/results.html',{'results_list':results_list,'products':results,'query':query})


def BusinessSearchView(request,query):
    results_list = Business.objects.filter(
        Q(name__icontains=query)|Q(description__icontains=query)
        )
    results_list = results_list.order_by('name')
    results = pager(request,results_list,12)
    return render(request,'Search/business_results.html',{'results_list':results_list,'businesses':results,'query':query})

# Renders the advanced Search page.
def AdvancedSearchView(request):
    SpecForm=ChooseSpecForm()
    return render(request,'Search/advanced_search_form.html',{'SpecForm':SpecForm})


def AdvancedSearchResultsView(request):
    price = request.GET.get('price','')
    mileage = request.GET.get('mileage','')
    car_type = request.GET.get('car_type','')
    brand = request.GET.get('brand','')
    # Need to filter out results so that sold vehicles do not appear in the search results. To do.
    if price or mileage or car_type or brand :
        results_list = Vehicle.objects.all()
        if mileage:
            results_list = results_list.filter(vehiclespec__mileage__lte=mileage).filter()
        if brand:
            results_list = results_list.filter(brand__name=brand)
        if car_type:
            results_list = results_list.filter(vehicle_type__name=car_type)
        if price:
            results_list = results_list.filter(price__lte=price)
        results_list = results_list.order_by('price')
    else:    
        results_list = Vehicle.objects.none()
    results = pager(request,results_list,12)
    context = {'results_list':results_list,'vehicles':results,"price":price,
        "car_type":car_type,"brand":brand,"mileage":mileage}
    return render(request,'Search/advanced_results.html',context)


def SearchAutocomplete(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = Product.objects.filter(name__icontains=query)
        prod_names = list()
        for product in qs:
            prod_names.append(product.name)
        return JsonResponse(prod_names,safe=False)



