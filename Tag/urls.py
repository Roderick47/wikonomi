from django.urls import path
from . import views

app_name="Tag"
urlpatterns = [
    path('tag/prod-add/<int:prod_id>',views.AddTagView,name='prod-add'),
    path('tag-autocomplete',views.TagAutocomplete,name='autocomplete'),
    path('tag-autocomplete-htmx',views.TagAutocompleteHtmx,name='autocomplete-htmx'),
    path('render-tag-chip',views.RenderTagChip,name='render-tag-chip'),
    path('tag/products/<int:tag_id>/<int:product_id>/',views.TagProductsView,name='products'),
]

