from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required

from .models import Notification
from Product.models import Product
from Comment.models import ProductComment


@login_required
def notification_list(request):
    """View to display all notifications for the current user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Notification/notification_list.html', {'notifications': notifications})


@login_required
def mark_all_read(request):
    """Mark all notifications as read for the current user."""
    if request.method == 'POST':
        updated = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).update(is_read=True)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'updated_count': updated})
        
        messages.success(request, f'Marked {updated} notifications as read.')
    
    return redirect('Notification:list')


@login_required
def mark_as_read(request, notification_id):
    """Mark a specific notification as read."""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        user=request.user
    )
    
    if not notification.is_read:
        notification.mark_as_read()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
    
    # Redirect to the appropriate content based on notification type
    if notification.notification_type in [Notification.COMMENT_REPLY, Notification.NEW_COMMENT] and notification.comment:
        return redirect(notification.comment.get_absolute_url())
    elif notification.product:
        return redirect(notification.product.get_absolute_url())
    
    return redirect('Notification:list')


@login_required
def delete_all(request):
    """Delete all notifications for the current user."""
    if request.method == 'POST':
        count, _ = Notification.objects.filter(user=request.user).delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'deleted_count': count})
        
        messages.success(request, f'Deleted {count} notifications.')
    
    return redirect('Notification:list')


@login_required
def notification_detail(request, notification_id):
    """View a specific notification and mark it as read."""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        user=request.user
    )
    
    # Mark as read when viewed
    if not notification.is_read:
        notification.mark_as_read()
    
    # Get related content based on notification type
    context = {'notification': notification}
    
    if notification.notification_type in [Notification.COMMENT_REPLY, Notification.NEW_COMMENT]:
        context['comment'] = notification.comment
        context['product'] = notification.product
    elif notification.product:
        context['product'] = notification.product
    
    return render(request, 'Notification/notification_detail.html', context)


@login_required
def get_unread_count(request):
    """API endpoint to get the count of unread notifications."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        return JsonResponse({'unread_count': count})
    return JsonResponse({'error': 'Invalid request'}, status=400)
