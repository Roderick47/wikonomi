from django.urls import path,include
from . import views


app_name='Profile'
urlpatterns = [
    path('profile',views.ProfileView,name='profile'),
    path('profile/public/<int:user_id>',views.PublicProfileView,name='public'),
    path('profile-update/<int:prof_id>',views.UpdateProfileView,name='update'),
    path('accounts/',include('allauth.urls'))  # all OAuth operations will be performed under this route
]
