from timeit import repeat
from django.shortcuts import render,redirect
from django.http import HttpResponse
import os
import mimetypes
import io
from django.core.paginator import Paginator

from WIKONOMI.settings import BASE_DIR

from .models import Product
from Business.models import Business
from .forms import ProductAddForm,GetOrCreateBusinessForm
from Photo.forms import ProductPhotoAddForm
from Post.models import Post
from Location.forms import LocationForm
from Location.models import Location
from Photo.models import ProductPhoto
from History.models import ProductHistory
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import JsonResponse
from Tag.models import Tag
from django.urls import reverse
from urllib.parse import urlencode
from tablib import Dataset
from .resources import ProductResource, UserProductResource
from itertools import repeat
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta


# Add product that is already linked to a business through bus_id.
def ProductAddView(request,bus_id):
    #Check to see if the user is authenticated. then returns back to their previous page.
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("account_login")
        next_url = reverse("Product:add",kwargs={"bus_id":bus_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
      
    if request.method == 'POST':
        form = ProductAddForm(request.POST,request.FILES)
        imageForm = ProductPhotoAddForm(request.POST,request.FILES)
        locationForm = LocationForm(request.POST)
        
        if form.is_valid() and imageForm.is_valid() and locationForm.is_valid():
            product = form.save(commit=False)
            product.business = Business.objects.get(id=bus_id)
            product.author = request.user
            
            # Handle location data from LocationForm
            latitude = locationForm.cleaned_data.get('latitude')
            longitude = locationForm.cleaned_data.get('longitude')
            
            # If we have coordinates, create or get a Location object
            if latitude is not None and longitude is not None:
                location_obj, created = Location.objects.get_or_create(
                    latitude=latitude,
                    longitude=longitude
                )
                product.location = location_obj
            
            product.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag.products.add(product)
            
            if imageForm.is_bound and imageForm.cleaned_data.get('photo'):
                ProductPhoto.objects.create(product=product, photo=imageForm.cleaned_data['photo'])
            
            # Handle social post creation
            social_post_body = form.cleaned_data.get('social_post')
            if social_post_body:
                Post.objects.create(
                    author=request.user,
                    body=social_post_body,
                    product=product
                )
                messages.success(request, 'Product and social post created successfully!')
            else:
                messages.success(request, 'Product added successfully!')

            return redirect('Product:detail',product.id)
        else:
            # Form validation failed - show errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductAddForm()
        imageForm = ProductPhotoAddForm()
        locationForm = LocationForm()
    
    business = Business.objects.get(id=bus_id)
    return render(request,'Product/ProductAddForm.html',{'form':form,'business':business,'imageForm':imageForm,'locationForm':locationForm})



# shows the detail of the product. 
def ProductDetailView(request,prod_id):
    product = get_object_or_404(Product, id=prod_id)
    productTags = Tag.objects.filter(products=product)
    
    # Get price history for the past year
   
    context = {
        'product': product,
        'productTags': productTags,
        'canonical_url': request.build_absolute_uri(
            reverse('Product:detail', kwargs={'prod_id': product.id})
        ),
    }
    return render(request,'Product/ProductDetail.html',context)



# Edits the product details.
def ProductEditView(request,prod_id):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can edit a product')
        base_url = reverse("account_login")
        next_url = reverse("Product:edit",kwargs={"prod_id":prod_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    product = get_object_or_404(Product,id=prod_id)
    try:
        # Get the first photo for this product, or None if no photos exist
        pic = ProductPhoto.objects.filter(product=product).first()
    except ProductPhoto.DoesNotExist:
        pic = None

    if request.method == 'POST':
        locationForm = LocationForm(request.POST)
        form = ProductAddForm(request.POST, request.FILES, instance=product)
        imageForm = ProductPhotoAddForm(request.POST, request.FILES)

        if form.is_valid() and imageForm.is_valid() and locationForm.is_valid():
            prod_instance = form.save(commit=False)
            
            # Handle location data - only set location if coordinates are provided
            if locationForm.cleaned_data.get('latitude') and locationForm.cleaned_data.get('longitude'):
                # Check if the location already exists
                location, created = Location.objects.get_or_create(
                    latitude=locationForm.cleaned_data['latitude'],
                    longitude=locationForm.cleaned_data['longitude']
                )
                # Assign the location to the product
                prod_instance.location = location
            else:
                # Keep existing location or set to None if no coordinates provided
                prod_instance.location = product.location
                
            prod_instance.author = request.user
            prod_instance.save()

            # Handle photo updates
            if imageForm.cleaned_data.get('photo'):
                # If a new photo is uploaded, update the existing one or create a new one
                if pic:
                    pic.photo = imageForm.cleaned_data['photo']
                    pic.save()
                else:
                    ProductPhoto.objects.create(photo=imageForm.cleaned_data['photo'], product=product)

            messages.success(request, 'Product updated successfully!')
            return redirect('Product:detail',prod_id)
        else:
            # Debug: Print form errors to see what's failing
            print("Form errors:")
            print("ProductAddForm errors:", form.errors)
            print("ImageForm errors:", imageForm.errors)
            print("LocationForm errors:", locationForm.errors)
        
    form = ProductAddForm(instance=product)
    imageForm = ProductPhotoAddForm()
    
    # Initialize location form with existing data
    location_instance = None
    if product.location:
        location_instance = {
            'latitude': product.location.latitude, 
            'longitude': product.location.longitude,
            'use_browser_location': False  # Set to False to avoid validation issues
        }
    else:
        location_instance = {'use_browser_location': False}  # Set to False to avoid validation issues
        
    locationForm = LocationForm(initial=location_instance)
    return render(request,'Product/ProductEditForm.html',{'form':form,'product':product,'imageForm':imageForm,'locationForm':locationForm})



# List the product of a particular business.
def BusinessProductListView(request,bus_id):
    business = Business.objects.get(id=bus_id)
    products = business.product_set.all().order_by('-date_created')
    return render(request,'Product/BusinessProductGallery.html',{'products':products,'business':business})



# Add a product not already linked to a business - this is done in this function.
def ProductAddGeneralView(request):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("account_login")
        next_url = reverse("Product:add-general")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    
    if request.method == 'POST':
        form = ProductAddForm(request.POST,request.FILES)
        form2 = GetOrCreateBusinessForm(request.POST)
        imageForm = ProductPhotoAddForm(request.POST,request.FILES)
        locationForm = LocationForm(request.POST)

        if form.is_valid() and form2.is_valid() and imageForm.is_valid() and locationForm.is_valid():
            product = form.save(commit=False)
            # Get of create a business and assign it to product instance.
            try:
                business = Business.objects.get_or_create(name=form2.cleaned_data['business'])[0]
            except:
                business = Business.objects.filter(name=form2.cleaned_data['business']).first()
            
            if not business:
                business = Business.objects.create(name=form2.cleaned_data['business'])
            #Test to see of the business is already selling that product.
            product_in_business = business.product_set.all().filter(name=product.name)

            if product_in_business:
                messages.add_message(request,messages.WARNING,'The product you tried to add is already sold by this business. You can edit this product if it has changed.')
                return redirect("Product:detail",product_in_business.first().id )
            
            # Handle location data from LocationForm
            latitude = locationForm.cleaned_data.get('latitude')
            longitude = locationForm.cleaned_data.get('longitude')
            
            # If we have coordinates, create or get a Location object
            if latitude is not None and longitude is not None:
                location_obj, created = Location.objects.get_or_create(
                    latitude=latitude,
                    longitude=longitude
                )
                product.location = location_obj
            
            # Assign the business and save the product.
            product.business = business
            product.author = request.user
            product.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag.products.add(product)

            # create the ProductPhoto for the product if there's one.

            if imageForm.is_bound and imageForm.cleaned_data.get('photo'):
                ProductPhoto.objects.create(product=product,photo=imageForm.cleaned_data['photo'])
            
            if imageForm.is_bound and imageForm.cleaned_data.get('photo'):
                ProductPhoto.objects.create(product=product,photo=imageForm.cleaned_data['photo'])
            
            # Handle social post creation
            social_post_body = form.cleaned_data.get('social_post')
            if social_post_body:
                Post.objects.create(
                    author=request.user,
                    body=social_post_body,
                    product=product
                )
                messages.success(request, 'Product and social post created successfully!')
            else:
                messages.success(request, 'Product added successfully!')

            return redirect('Product:detail',product.id)
        
    form = ProductAddForm()
    form2 = GetOrCreateBusinessForm()
    imageForm = ProductPhotoAddForm()
    locationForm = LocationForm()
    return render(request,'Product/GeneralProductAddForm.html',{'form':form,'form2':form2,'imageForm':imageForm,'locationForm':locationForm})



def ProductDeleteView(request,prod_id):
    #The delete button is only rendered if the user is authenticated.
    if request.user.is_authenticated:
        product = Product.objects.get(id=prod_id)
        product.delete()
        return redirect('Home:home')
    return redirect('Product:detail',prod_id)



# Download a csv file temlate to be used in another view funciton to add a multiple products.
def ProductListTemplateDownload(request):
    filename = 'file_download/product_list_template.xlsx'
    filepath = os.path.join(BASE_DIR,filename) # MAke sure to change this filepath on deployment.
    path = open(filepath,'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path,content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response



# Upload a csv file with a product name,price,detail and using the file we generate new products.
def ProductListUpload(request, bus_id):
    """
    Secure file upload for bulk product creation.
    Validates file type, size, user authorization, and data integrity.
    """
    import logging
    from django.db import transaction
    from django.core.cache import cache
    
    logger = logging.getLogger(__name__)
    
    # Authentication check
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You need to login before you can add a Product.')
        base_url = reverse("account_login")
        next_url = reverse("Product:list-upload", kwargs={"bus_id": bus_id})
        next = urlencode({"next": next_url})
        url = '{}?{}'.format(base_url, next)
        return redirect(url)
    
    # Authorization check - verify business exists and handle public/private distinction
    try:
        business = Business.objects.get(id=bus_id)
    except Business.DoesNotExist:
        messages.error(request, 'Business not found.')
        logger.warning(f'User {request.user.username} attempted to upload to non-existent business {bus_id}')
        return redirect('Home:home')

    # For private businesses, only the owner can upload products
    # For public businesses, anyone can upload products (since anyone can edit public business info)
    if not business.is_public and business.author != request.user:
        messages.error(request, 'You do not have permission to add products to this private business.')
        logger.warning(f'User {request.user.username} attempted unauthorized upload to private business {bus_id}')
        return redirect('Business:detail', bus_id=bus_id)
    
    if request.method == 'POST':
        # Rate limiting: max 5 uploads per hour per user
        cache_key = f'product_upload_limit_{request.user.id}'
        upload_count = cache.get(cache_key, 0)
        
        if upload_count >= 5:
            messages.error(request, 'Upload limit reached (5 per hour). Please try again later.')
            logger.warning(f'User {request.user.username} exceeded upload rate limit')
            return render(request, "Product/import_product_list.html", {'business': business})
        
        new_products = request.FILES.get('myfile', False)
        
        if not new_products:
            messages.error(request, 'Please select a file to upload.')
            return render(request, "Product/import_product_list.html", {'business': business})
        
        # File validation
        ALLOWED_EXTENSIONS = ['.xlsx', '.xls']
        ALLOWED_MIME_TYPES = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel'
        ]
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        MAX_PRODUCTS = 1000  # Maximum products per upload
        
        # Validate file extension
        file_ext = os.path.splitext(new_products.name)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            messages.error(request, 'Invalid file type. Only .xlsx and .xls files are allowed.')
            logger.warning(f'User {request.user.username} attempted to upload invalid file type: {file_ext}')
            return render(request, "Product/import_product_list.html", {'business': business})
        
        # Validate MIME type
        if new_products.content_type not in ALLOWED_MIME_TYPES:
            messages.error(request, 'Invalid file format. Please upload a valid Excel file.')
            logger.warning(f'User {request.user.username} uploaded file with invalid MIME type: {new_products.content_type}')
            return render(request, "Product/import_product_list.html", {'business': business})
        
        # Validate file size
        if new_products.size > MAX_FILE_SIZE:
            messages.error(request, f'File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB.')
            logger.warning(f'User {request.user.username} attempted to upload file larger than {MAX_FILE_SIZE} bytes')
            return render(request, "Product/import_product_list.html", {'business': business})
        
        try:
            # Read the uploaded file using BytesIO
            file_buffer = io.BytesIO(new_products.read())
            
            # Use transaction to ensure atomic operation
            with transaction.atomic():
                product_resource = ProductResource()
                dataset = Dataset()
                
                # Load and parse the Excel file
                try:
                    imported_data = dataset.load(file_buffer, format='xlsx', headers=True)
                except Exception as e:
                    messages.error(request, 'Failed to read Excel file. Please ensure it is a valid Excel file.')
                    logger.error(f'Excel parsing error for user {request.user.username}: {str(e)}')
                    return render(request, "Product/import_product_list.html", {'business': business})
                
                # Validate number of products
                if len(imported_data) == 0:
                    messages.error(request, 'The uploaded file contains no data.')
                    return render(request, "Product/import_product_list.html", {'business': business})
                
                if len(imported_data) > MAX_PRODUCTS:
                    messages.error(request, f'Too many products. Maximum {MAX_PRODUCTS} products per upload.')
                    logger.warning(f'User {request.user.username} attempted to upload {len(imported_data)} products')
                    return render(request, "Product/import_product_list.html", {'business': business})
                
                # Create lists for additional fields
                author_list, business_list, is_public_list = [], [], []
                author_list.extend(repeat(request.user.id, len(imported_data)))
                business_list.extend(repeat(bus_id, len(imported_data)))
                is_public_list.extend(repeat(1, len(imported_data)))
                
                # Append additional columns
                imported_data.append_col(author_list, header='author')
                imported_data.append_col(business_list, header='business')
                imported_data.append_col(is_public_list, header='is_public')
                
                # Dry run to validate data
                result = product_resource.import_data(imported_data, dry_run=True, raise_errors=False)
                
                if result.has_errors():
                    # Collect and display errors
                    error_messages = []
                    for row_errors in result.row_errors():
                        row_num = row_errors[0]
                        errors = row_errors[1]
                        for error in errors:
                            error_messages.append(f'Row {row_num}: {error.error}')
                    
                    # Display first 5 errors
                    for error_msg in error_messages[:5]:
                        messages.error(request, error_msg)
                    
                    if len(error_messages) > 5:
                        messages.warning(request, f'... and {len(error_messages) - 5} more errors.')
                    
                    logger.warning(f'Import validation failed for user {request.user.username}: {len(error_messages)} errors')
                    return render(request, "Product/import_product_list.html", {'business': business})
                
                # If validation passed, perform actual import
                result = product_resource.import_data(imported_data, dry_run=False, raise_errors=False)
                
                if result.has_errors():
                    messages.error(request, 'An error occurred during import. Please try again.')
                    logger.error(f'Import failed for user {request.user.username} on business {bus_id}')
                    return render(request, "Product/import_product_list.html", {'business': business})
                
                # Success - increment rate limit counter
                cache.set(cache_key, upload_count + 1, 3600)  # 1 hour timeout
                
                # Log success
                logger.info(f'User {request.user.username} successfully uploaded {len(imported_data)} products to business {bus_id}')
                
                messages.success(request, f'Successfully imported {len(imported_data)} products.')
                return redirect("Product:business-list", bus_id)
        
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            logger.error(f'Unexpected error during product upload for user {request.user.username}: {str(e)}')
            return render(request, "Product/import_product_list.html", {'business': business})
    
    return render(request, "Product/import_product_list.html", {'business': business})

    

def ProductAutocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term')).order_by('date_created')
        prod_names = list()
        for product in qs:
            prod_names.append(product.name)
        return JsonResponse(prod_names,safe=False)


def test_view(request):
    """Simple test view to debug encoding issues"""
    return render(request, 'Product/test.html', {})


# Returns all products for browsing.
def AllProductListView(request):
    products = Product.objects.filter(date_updated__lt=datetime.now()).order_by('-date_created')
    return render(request,'Product/allProducts.html',{'all_products':products})
