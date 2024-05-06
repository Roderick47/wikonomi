from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode

from .models import Notification


def NotificationListView(request):
    if not  request.user.is_authenticated:
        return redirect('Home:home')
    notifications = Notification.objects.filter(user=request.user).order_by('id')
    return render(request,'Notification/notification_list.html',{'notifications':notifications})

def ReadAllView(request):
    #Check to see if the user is authenticated. then returns back to their previous page.
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("Profile:login")
        next_url = reverse("Notification:list")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    all_notifications = Notification.objects.filter(user=request.user)
    for notification in all_notifications:
        notification.is_viewed = True
        notification.save()
    return redirect('Notification:list')

def DeleteAllView(request):
    #Check to see if the user is authenticated. then returns back to their previous page.
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("Profile:login")
        next_url = reverse("Notification:list")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    all_notifications = Notification.objects.filter(user=request.user)
    for notification in all_notifications:
        notification.delete()
    return redirect('Notification:list')
