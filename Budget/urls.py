from django.urls import path
from . import views

app_name="Budget"
urlpatterns = [
    path('list',views.BudgetListView,name='list'),
    path('detail/<int:budg_id>',views.BudgetDetailView,name="detail"),
    path('create',views.CreateBudgetView,name='create'),

]
