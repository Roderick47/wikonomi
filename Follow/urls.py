from django.urls import path
from . import views

app_name="Follow"
urlpatterns = [
    path('follow/<int:prod_id>',views.FollowView,name='follow'),
    path('unfollow/<int:prod_id>',views.UnfollowView,name='unfollow'),
    path('my-watch-list',views.SubscriptionsView,name='subscriptions'),
]
