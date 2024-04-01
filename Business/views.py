from django.shortcuts import render,redirect
from .models import Business
from .forms import BusinessAddForm
from django.db.models import Avg,Q
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import datetime
from urllib.parse import urlencode

# Create your views here.


def BusinessAddView(request):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,'You need to login before you can add a business')
        base_url = reverse("Profile:login")
        next_url = reverse("Business:add")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)

    if request.method == 'POST':
        form = BusinessAddForm(request.POST,request.FILES)
        if form.is_valid():
            business=form.save(commit=False)
            business.author = request.user
            business.save()
            return redirect('Business:detail',business.id)
    else:
        form = BusinessAddForm()
    return render(request,'Business/BusinessAddForm.html',{'form':form})

def BusinessEditView(request,bus_id):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,'You need to login before you can add a business')
        base_url = reverse("Profile:login")
        next_url = reverse("Business:edit",kwargs={"bus_id":bus_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    business = Business.objects.get(id=bus_id)
    if request.method == 'POST':
        form = BusinessAddForm(request.POST,request.FILES)
        if form.is_valid():
            edit=form.save(commit=False)
            if edit.image:
                business.image = edit.image
            business.name = edit.name
            business.description = edit.description
            business.location = edit.location
            business.author = request.user
            business.save()
            return redirect('Business:detail',bus_id)
    form = BusinessAddForm(instance=business)
    return render(request,'Business/BusinessEditForm.html',{'form':form,'business':business})

# Renders the Public Business detail page with the review form as well.
def BusinessDetailView(request,bus_id):
    business = Business.objects.get(id=bus_id)
    products = business.product_set.all()
    return render(request,'Business/BusinessDetail.html',{'business':business,'products':products,})


# No tests for this view yet.
def BusinessAutocomplete(request):
    if 'term' in request.GET:
        qs = Business.objects.filter(name__icontains=request.GET.get('term')).order_by('date_created')
        biz_names = list()
        for business in qs:
            biz_names.append(business.name)
        return JsonResponse(biz_names,safe=False)


def PrivateBusinessAddView(request):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,'You need to login before you can add a business')
        base_url = reverse("Profile:login")
        next_url = reverse("Business:add-private")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    
    if request.method == 'POST':
        form = BusinessAddForm(request.POST,request.FILES)
        if form.is_valid():
            business=form.save(commit=False)
            business.author = request.user
            business.is_public = False
            business.save()
            return redirect('Home:home')
    form = BusinessAddForm()
    return render(request,'Business/PrivateBusinessAddForm.html',{'form':form})

# Returns all businesses.
def AllBusinessListView(request):
    businesses = Business.objects.filter(date_updated__lt=datetime.datetime.now()).order_by('-date_created')
    return render(request,'Business/allBusiness.html',{'all_business':businesses})
