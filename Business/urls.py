from django.urls import path,re_path
from . import views

app_name='Business'
urlpatterns = [
    path('Business/public/detail/<int:bus_id>',views.BusinessDetailView, name='detail'),
    path('Business/public/add',views.BusinessAddView, name='add'),
    path('Business/private/add',views.PrivateBusinessAddView, name='add-private'),
    path('Business/public/edit/<int:bus_id>',views.BusinessEditView, name='edit'),
    path('business-autocomplete',views.BusinessAutocomplete, name='autocomplete'),
    path('Business/all',views.AllBusinessListView, name='all'),
    ]