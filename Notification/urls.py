from django.urls import path
from django.views.decorators.http import require_http_methods
from . import views

app_name = "Notification"

urlpatterns = [
    # List all notifications
    path('notifications/', views.notification_list, name='list'),
    
    # Mark all notifications as read
    path('notifications/mark-all-read/', 
         views.mark_all_read, 
         name='mark_all_read'),
    
    # Mark a single notification as read
    path('notifications/<int:notification_id>/mark-read/', 
         views.mark_as_read, 
         name='mark_read'),
    
    # View notification details
    path('notifications/<int:notification_id>/', 
         views.notification_detail, 
         name='detail'),
    
    # Delete all notifications
    path('notifications/delete-all/', 
         require_http_methods(['POST'])(views.delete_all), 
         name='delete_all'),
    
    # API endpoint to get unread count (for AJAX)
    path('api/notifications/unread-count/', 
         views.get_unread_count, 
         name='unread_count'),
]
