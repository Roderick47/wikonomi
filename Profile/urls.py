from django.urls import path
from . import views

app_name='Profile'
urlpatterns = [
    path('profile',views.ProfileView,name='profile'),
    path('profile/public/<int:user_id>',views.PublicProfileView,name='public'),
    path('login',views.LoginView,name='login'),
    path('logout',views.LogoutView,name='logout'),
    path('signup',views.SignupView,name='signup'),
    path('profile-update/<int:prof_id>',views.UpdateProfileView,name='update'),

]
