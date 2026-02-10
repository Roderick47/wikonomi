from django.urls import path
from . import views

app_name="Location"
urlpatterns = [
    path('location/product/<int:location_id>',views.LocationView, name='location'),
    path('location/business/<int:location_id>',views.BusinessLocationView, name='business'),
    path('api/nearby-businesses/<int:location_id>/',views.get_nearby_businesses, name='nearby-businesses'),
    path('api/reverse-geocode/', views.reverse_geocode, name='reverse_geocode'),
]