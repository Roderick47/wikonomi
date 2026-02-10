from django.contrib import admin
from .models import BugReport

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'url_route')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'priority')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Report Details', {
            'fields': ('title', 'description', 'expected_behavior', 'url_route', 'screenshot', 'user')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
