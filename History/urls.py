from django.urls import path
from . import views

app_name="History"
urlpatterns = [
    path('history/product/<int:his_id>',views.ProductHistoryDetailView,name='edit-detail'),
    path("history/edit/list/<int:prod_id>",views.ProductEditHistoryView,name="edit-list"),
]
