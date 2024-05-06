from django.contrib import admin
from .models import ProductHistory


class ProductHistoryAdmin(admin.ModelAdmin):
    #fields = ['product','name','description','previous_author' ,'current_author','price','date_created','date_updated','business','is_public']
    list_display = ('__str__','product','business','current_author','previous_author',)
    search_fields = ['name']
    # actions = []
    # def action(self,request,queryset)

admin.site.register(ProductHistory,ProductHistoryAdmin)
