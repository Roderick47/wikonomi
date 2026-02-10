from django.shortcuts import render
from django.http import JsonResponse
from Product.models import Product
from Business.models import Business
from .models import Location
from django.db.models import Q
import math

# Create your views here.

def LocationView(request, location_id=None):
    """Display location details with map"""
    location = Location.objects.get(id=location_id)
    
    # Get businesses at this location (using the new ForeignKey relationship)
    businesses = Business.objects.filter(location=location)
    
    # Get products from businesses at this location
    products = Product.objects.filter(business__in=businesses)
    
    context = {
        'location': location,
        'businesses': businesses,
        'products': products,
    }
    return render(request, 'Location/location.html', context)

def BusinessLocationView(request, location_id=None):
    """Display business location details"""
    location = Location.objects.get(id=location_id)
    
    # Get businesses at this location (using the new ForeignKey relationship)
    businesses = Business.objects.filter(location=location)
    
    context = {
        'location': location,
        'businesses': businesses,
    }
    return render(request, 'Location/location.html', context)

def get_nearby_businesses(request, location_id):
    """API endpoint to get nearby businesses"""
    try:
        location = Location.objects.get(id=location_id)
        
        # Calculate nearby businesses (within ~5km radius)
        # This is a simple calculation - you might want to use PostGIS for better performance
        nearby_businesses = []
        
        # Get all businesses with locations (using the new ForeignKey relationship)
        all_businesses = Business.objects.exclude(location__isnull=True)
        
        for business in all_businesses:
            # Try to extract coordinates from business location
            # This is a simplified approach - you might want to store coordinates separately
            if business.location:
                # For now, just return businesses that have location data
                nearby_businesses.append({
                    'id': business.id,
                    'name': business.name,
                    'description': business.description,
                    'location_description': business.location_description,
                    'url': business.get_absolute_url() if hasattr(business, 'get_absolute_url') else None,
                })
        
        return JsonResponse({
            'success': True,
            'businesses': nearby_businesses[:10]  # Limit to 10 nearby businesses
        })
        
    except Location.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Location not found'
        })

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


# Proxy view for reverse geocoding to avoid CORS issues
import requests
from django.views.decorators.http import require_GET

@require_GET
def reverse_geocode(request):
    """Fetch address from Nominatim and return JSON.
    Expects 'lat' and 'lon' query parameters.
    """
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return JsonResponse({'error': 'Missing lat or lon'}, status=400)
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'format': 'json',
        'lat': lat,
        'lon': lon,
        'zoom': 18,
        'addressdetails': 1,
    }
    headers = {
        'User-Agent': 'Wikonomi/1.0 (location-selector)'
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
