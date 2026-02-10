from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    # Main feed - Removed: Posts are now shown in the main home feed
    # path('', views.post_feed, name='feed'),
    
    # Create/Edit/Delete
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('<int:post_id>/edit/', views.edit_post, name='edit'),
    path('<int:post_id>/delete/', views.delete_post, name='delete'),
    
    # Interactions
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # User posts
    path('user/<str:username>/', views.user_posts, name='user_posts'),
]
