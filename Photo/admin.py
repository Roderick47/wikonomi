from django.contrib import admin
from .models import ProductPhoto,BusinessPhoto
# Register your models here.

class BusinessPhotoAdmin(admin.ModelAdmin):
    fields = ['business','photo']
    ordering = ['business','photo']
    list_display = ('business','photo')
    search_fields = ['photo']
    #actions = []
    #def action(self,request,queryset)

class ProductPhotoAdmin(admin.ModelAdmin):
    fields = ['product','photo']
    ordering = ['product','photo']
    list_display = ('product','photo')
    search_fields = ['photo']
    #actions = []
    #def action(self,request,queryset)

admin.site.register(ProductPhoto,ProductPhotoAdmin)
admin.site.register(BusinessPhoto,BusinessPhotoAdmin)
