from django.urls import path
from . import views

app_name="Search"
urlpatterns = [
    path('results',views.SearchView,name='search'),
    path('search-autocomplete',views.SearchAutocomplete,name='autocomplete'),
    path('results/business/<str:query>',views.BusinessSearchView,name='search-business'),
    # path('advanced-results',views.AdvancedSearchResultsView,name='advanced-results'),
]
