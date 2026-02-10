from django.urls import path
from . import views

app_name = "Budget"

urlpatterns = [
    path('', views.BudgetListView, name='list'),
    path('<int:budg_id>/', views.BudgetDetailView, name="detail"),
    
    # HTMX Partials & Actions
    path('hx/create-modal/', views.hx_create_budget_modal, name='hx_create_budget_modal'),
    path('hx/save-budget/', views.hx_save_budget, name='hx_save_budget'),
    path('hx/tab/<int:budg_id>/<str:tab_name>/', views.hx_budget_tab, name='hx_tab'),
    path('hx/add-category-row/', views.hx_add_category_row, name='hx_add_category_row'),
    path('hx/save-category/<int:budg_id>/', views.hx_save_category, name='hx_save_category'),
    path('hx/delete-category/<int:cat_id>/', views.hx_delete_category, name='hx_delete_category'),
    path('hx/add-item/<int:budg_id>/', views.hx_add_item_to_shopping_list, name='hx_add_item'),
    path('hx/update-item/<int:item_id>/', views.hx_update_item, name='hx_update_item'),
    path('hx/delete-item/<int:item_id>/', views.hx_delete_item, name='hx_delete_item'),
    path('hx/product-search/', views.product_search, name='product_search'),
    path('hx/refresh-prices/<int:budg_id>/', views.hx_refresh_prices, name='hx_refresh_prices'),
]
