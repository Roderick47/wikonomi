from django.urls import path
from . import views

app_name="Home"
urlpatterns = [
    path('',views.HomeView,name='home'),
    path('About',views.AboutView,name="about"),
    path('welcome/', views.WelcomeView, name='welcome'),
    path('welcome/continue/', views.WelcomeContinueView, name='welcome-continue'),
    path('welcome/explore/', views.WelcomeExploreView, name='welcome-explore'),
]
