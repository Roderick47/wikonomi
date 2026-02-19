"""WIKONOMI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from Follow.views import api_toggle_watchlist

urlpatterns = [
    path('', include('Home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('Profile.urls')),
    path('', include('Business.urls')),
    path('', include('Product.urls')),
    path('', include('Comment.urls')),
    path('', include('Tag.urls')),
    path('', include('Follow.urls')),  # Keep existing URLs for backward compatibility
    path('api/toggle-watchlist/<int:product_id>/', api_toggle_watchlist, name='api_toggle_watchlist'),
    path('', include('Search.urls')),
    path('', include('Notification.urls')),
    path('', include('History.urls')),
    path('', include('Location.urls')),
    path('budget/', include('Budget.urls')),
    path('post/', include('Post.urls')),
    path('qa/', include('QA.urls')),
    path('report/', include('Report.urls')),
    path('howto/', include('HowTo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

if not settings.DEBUG and getattr(settings, 'RENDER_DISK_PATH', None):
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Force server reload for new templates
