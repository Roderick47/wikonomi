from django.contrib import admin
from .models import Notification
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('__str__','created_at','user','is_read','product','comment','data')
    search_fields = ['user']
    # actions = []
    # def action(self,request,queryset)

admin.site.register(Notification,NotificationAdmin)