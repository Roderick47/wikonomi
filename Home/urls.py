from django.urls import path
from . import views

app_name="Home"
urlpatterns = [
    path('',views.HomeView,name='home'),
    path('About',views.AboutView,name="about"),
]
