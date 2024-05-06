from django.urls import path
from . import views

app_name="Location"
urlpatterns = [
    path('location/product/<int:location_id>',views.LocationView, name='location'),
    # path('location/business/<int:location_id>',views.BusinessLocationView, name='business'),
]