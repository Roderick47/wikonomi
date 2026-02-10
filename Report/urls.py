from django.urls import path
from . import views

app_name = 'Report'

urlpatterns = [
    path('bug/', views.report_bug, name='bug'),
    path('success/', views.report_success, name='success'),
]
