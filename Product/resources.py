from import_export import resources
from import_export.fields import Field
from .models import Product
from django.core.exceptions import ValidationError
import bleach


class ProductResource(resources.ModelResource):
    
    def before_import_row(self, row, **kwargs):
        """Validate and sanitize data before importing"""
        # Validate price
        try:
            price = float(row.get('price', 0))
            if price < 0:
                raise ValidationError('Price cannot be negative')
            if price > 10000000:  # 10 million max
                raise ValidationError('Price exceeds maximum allowed value')
        except (ValueError, TypeError):
            raise ValidationError('Price must be a valid number')
        
        # Validate and sanitize name
        name = str(row.get('name', '')).strip()
        if not name:
            raise ValidationError('Product name is required')
        if len(name) > 100:
            raise ValidationError('Product name cannot exceed 100 characters')
        # Sanitize name to prevent XSS
        row['name'] = bleach.clean(name, tags=[], strip=True)
        
        # Validate and sanitize description
        description = str(row.get('description', '')).strip()
        if len(description) > 300:
            description = description[:300]
        # Sanitize description to prevent XSS
        row['description'] = bleach.clean(description, tags=[], strip=True)
    
    class Meta:
        model = Product
        import_id_fields = []  # Don't use id for matching during import
        skip_unchanged = True
        report_skipped = True
        fields = ('name', 'price', 'description')  # Only import fields that are in the Excel file


class UserProductResource(resources.Resource):
    name = Field(column_name='name')
    description = Field(column_name='description')
    price = Field(column_name='price')

    class Meta:
        export_order = ('name','price','description')




