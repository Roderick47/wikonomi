from import_export import resources
from import_export.fields import Field
from .models import Product

class ProductResource(resources.ModelResource):
    
    class Meta:
        model=Product
    


class UserProductResource(resources.Resource):
    name = Field(column_name='name')
    description = Field(column_name='description')
    price = Field(column_name='price')

    class Meta:
        export_order = ('name','price','description')




