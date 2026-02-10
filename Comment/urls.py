from django.urls import path
from . import views

app_name = 'Comment'

urlpatterns = [
    # New comment system URLs
    path('list/', views.CommentListView.as_view(), name='list'),
    path('create/', views.CommentCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', views.CommentEditView.as_view(), name='edit'),
    path('update/<int:pk>/', views.CommentUpdateView.as_view(), name='update'),
    path('<int:parent_id>/replies/', views.CommentRepliesView.as_view(), name='replies'),
    
    # Legacy URLs for backward compatibility (can be removed later)
    path('product/<int:prod_id>/post/', views.ProductCommentView, name='prod-post'),
    path('product/<int:prod_id>/load-more/', views.LoadMoreComments, name='load-more'),
    path('product/<int:com_id>/delete/', views.DeleteProductCommentView, name='prod-delete'),
    path('product/<int:com_id>/seek/', views.SeekCommentView, name='prod-seek'),
]
