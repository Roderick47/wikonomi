from django.urls import path
from . import views

app_name="Product"
urlpatterns = [
    path('product/public/add',views.ProductAddGeneralView,name='add-general'),
    path('product/detail/<int:prod_id>',views.ProductDetailView,name='detail'),
    path('business/products/<int:bus_id>',views.BusinessProductListView,name='business-list'),
    path('product/public/edit/<int:prod_id>',views.ProductEditView,name='edit'),
    path('product/public/delete/<int:prod_id>',views.ProductDeleteView,name='delete'),
    path('product-autocomplete',views.ProductAutocomplete,name='autocomplete'),
    path('product/list/upload/<int:bus_id>',views.ProductListUpload,name='list-upload'),
    path('product/list/template/download',views.ProductListTemplateDownload,name='template-download'),
    path('product/add/<int:bus_id>',views.ProductAddView,name='add'),

    
]
