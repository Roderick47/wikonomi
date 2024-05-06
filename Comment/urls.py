from django.urls import path
from . import views

app_name="Comment"
urlpatterns = [
    path('product-comment/<int:prod_id>',views.ProductCommentView,name='prod-post'),
    path('product-comment-delete/<int:com_id>',views.DeleteProductCommentView,name='prod-delete'),
    path('product-comment-seek/<int:com_id>',views.SeekCommentView,name='seek'),
]
