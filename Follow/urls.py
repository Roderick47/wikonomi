from django.urls import path
from . import views

app_name="Follow"
urlpatterns = [
    path('follow/<int:prod_id>', views.FollowProductView, name='follow'),
    path('unfollow/<int:prod_id>', views.UnfollowView, name='unfollow'),
    path('my-watch-list', views.SubscriptionsView, name='subscriptions'),
    path('watchlist', views.WatchlistView, name='watchlist'),
    # API Endpoints
    path('api/toggle-watchlist/<int:product_id>/', views.api_toggle_watchlist, name='api_toggle_watchlist'),
]
