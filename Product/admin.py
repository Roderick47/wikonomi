from django.contrib import admin
from import_export.admin import ImportExportModelAdmin 
from .models import Product
# Register your models here.

class ProductAdmin(ImportExportModelAdmin):
    fields = ['name','description','price','author','business','is_public']
    ordering = ['name','description','price','author','business']
    list_display = ('name','description','price','author','business','is_public')
    search_fields = ['name']
    #actions = []
    #def action(self,request,queryset)



admin.site.register(Product,ProductAdmin)
