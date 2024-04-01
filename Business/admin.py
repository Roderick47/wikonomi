from django.contrib import admin
from .models import Business


class BusinessAdmin(admin.ModelAdmin):
    fields = ['name','image','description','location','author','is_public',]
    ordering = ['name','image','description','location','author','is_public']
    list_display = ('name','description','location','author','is_public')
    search_fields = ['name']
    # actions = []
    # def action(self,request,queryset)



admin.site.register(Business,BusinessAdmin)
