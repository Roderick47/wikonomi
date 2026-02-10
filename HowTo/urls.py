from django.urls import path
from . import views

app_name = 'HowTo'

urlpatterns = [
    path('', views.HowToListView, name='list'),
    path('create/', views.HowToCreateView, name='create'),
    path('<int:how_id>/', views.HowToDetailView, name='detail'),
    path('<int:how_id>/edit/', views.HowToEditView, name='edit'),
    path('<int:how_id>/history/', views.HowToHistoryView, name='history'),
    path('<int:how_id>/toggle-official/', views.HowToOfficialToggle, name='toggle-official'),
    path('product/<int:product_id>/', views.ProductGuidesView, name='product-guides'),
    path('business/<int:business_id>/', views.BusinessGuidesView, name='business-guides'),
]
