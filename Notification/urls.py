from django.urls import path
from . import views

app_name="Notification"
urlpatterns = [
    path('notifications',views.NotificationListView,name='list'),
    path('notifications/read-all',views.ReadAllView,name="read-all"),
    path('notifications/delete-all',views.DeleteAllView,name="delete-all"),

]
