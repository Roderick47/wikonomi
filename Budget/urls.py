from django.urls import path
from . import views

app_name="Budget"
urlpatterns = [
    path('list', views.BudgetListView, name='list'),
    path('detail/<int:budg_id>', views.BudgetDetailView, name="detail"),
    path('create', views.CreateBudgetView, name='create'),
    # API Endpoints
    path('api/list/', views.api_list_budgets, name='api_list_budgets'),
    path('api/add-product/<int:budget_id>/<int:product_id>/', views.api_add_to_budget, name='api_add_to_budget'),
]
