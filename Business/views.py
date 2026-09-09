from django.shortcuts import render,redirect
from .models import Business
from .forms import BusinessAddForm
from django.db.models import Avg,Q
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import datetime
from urllib.parse import urlencode
from Location.models import Location
from Location.models import Location
from Post.models import Post
from Tag.models import Tag
import requests

# Create your views here.

def get_address_from_coordinates(lat, lng):
    """Get address from GPS coordinates using OpenStreetMap Nominatim"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=18&addressdetails=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', '')
    except Exception as e:
        print(f"Reverse geocoding error: {e}")
    return ''

def BusinessAddView(request):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,'You need to login before you can add a business')
        base_url = reverse("account_login")
        next_url = reverse("Business:add")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)

    if request.method == 'POST':
        form = BusinessAddForm(request.POST,request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.author = request.user

            # Handle GPS coordinates from request.POST (not form.cleaned_data since they're not in the form)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            location_text = request.POST.get('id_location', '')

            if latitude and longitude:
                # Get address from GPS if location text is empty
                if not location_text:
                    display_name = get_address_from_coordinates(float(latitude), float(longitude))
                    if not display_name:
                        display_name = f"GPS: {latitude}, {longitude}"
                    # Update the location field with the display name
                    business.location_name = display_name

                # Create or get a Location object with just latitude and longitude
                location_obj, created = Location.objects.get_or_create(
                    latitude=float(latitude),
                    longitude=float(longitude)
                )
                business.location = location_obj

            business.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag.businesses.add(business)
            
            # Handle social post creation
            social_post_body = form.cleaned_data.get('social_post')
            if social_post_body:
                Post.objects.create(
                    author=request.user,
                    body=social_post_body,
                    business=business
                )
                messages.success(request, 'Business and social post created successfully with GPS location!')
            else:
                messages.success(request, 'Business created successfully with GPS location!')

            return redirect('Business:detail',business.id)
    else:
        form = BusinessAddForm()
    return render(request,'Business/BusinessAddForm.html',{'form':form})

def BusinessEditView(request,bus_id):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,'You need to login before you can add a business')
        base_url = reverse("account_login")
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
            
            # Handle GPS coordinates from request.POST
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            location_text = request.POST.get('location', '')  # Changed from id_location to location
            
            if latitude and longitude:
                # Get address from GPS if location text is empty
                if not location_text:
                    display_name = get_address_from_coordinates(float(latitude), float(longitude))
                    if not display_name:
                        display_name = f"GPS: {latitude}, {longitude}"
                    # Update the location description field
                    business.location_description = display_name
                else:
                    business.location_description = location_text

                # Create or get a Location object with just latitude and longitude
                location_obj, created = Location.objects.get_or_create(
                    latitude=float(latitude),
                    longitude=float(longitude)
                )
                business.location = location_obj
            else:
                # If no coordinates, clear the location
                business.location = None
                business.location_description = location_text if location_text else ''
            
            business.author = request.user
            business.save()
            messages.success(request, 'Business updated successfully with GPS location!')
            return redirect('Business:detail',bus_id)
        
    form = BusinessAddForm(instance=business)
    return render(request,'Business/BusinessEditForm.html',{'form':form,'business':business})



# Renders the business detail page (anyone can view any business).
def BusinessDetailView(request,bus_id):
    business = Business.objects.get(id=bus_id)
    products = business.product_set.all()
    return render(request,'Business/BusinessDetail.html',{
        'business': business,
        'products': products,
        'canonical_url': request.build_absolute_uri(
            reverse('Business:detail', kwargs={'bus_id': business.id})
        ),
    })


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
        base_url = reverse("account_login")
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

            # Handle GPS coordinates from request.POST
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            location_text = request.POST.get('id_location', '')

            if latitude and longitude:
                # Get address from GPS if location text is empty
                if not location_text:
                    display_name = get_address_from_coordinates(float(latitude), float(longitude))
                    if not display_name:
                        display_name = f"GPS: {latitude}, {longitude}"
                    # Update the location field with the display name
                    business.location_name = display_name

                # Create or get a Location object with just latitude and longitude
                location_obj, created = Location.objects.get_or_create(
                    latitude=float(latitude),
                    longitude=float(longitude)
                )
                business.location = location_obj

            business.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag.businesses.add(business)
            
            # Handle social post creation
            social_post_body = form.cleaned_data.get('social_post')
            if social_post_body:
                Post.objects.create(
                    author=request.user,
                    body=social_post_body,
                    business=business
                )
                messages.success(request, 'Private business and social post created successfully!')
            else:
                messages.success(request, 'Private business created successfully!')

            return redirect('Home:home')
    form = BusinessAddForm()
    return render(request,'Business/PrivateBusinessAddForm.html',{'form':form})

# Returns all businesses (both public and private) for browsing.
def AllBusinessListView(request):
    businesses = Business.objects.filter(date_updated__lt=datetime.datetime.now()).order_by('-date_created')
    return render(request,'Business/allBusiness.html',{'all_business':businesses})

# Returns businesses owned by the current user (both public and private)
def MyBusinessListView(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You need to login to view your businesses.')
        base_url = reverse("account_login")
        next_url = reverse("Business:my-businesses")
        next = urlencode({"next": next_url})
        url = '{}?{}'.format(base_url, next)
        return redirect(url)

    businesses = Business.objects.filter(author=request.user).order_by('-date_created')
    return render(request,'Business/allBusiness.html',{'all_business':businesses, 'is_owner_view': True})

def BusinessDeleteView(request,bus_id):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,'You need to login before you can add a business')
        base_url = reverse("account_login")
        next_url = reverse("Business:delete",kwargs={"bus_id":bus_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
