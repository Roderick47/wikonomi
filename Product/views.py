from timeit import repeat
from django.shortcuts import render,redirect
from django.http import HttpResponse
import os
import mimetypes
import io

from WIKONOMI.settings import BASE_DIR

from .models import Product
from Comment.models import ProductComment
# from Comment.models import ProductComment
from Business.models import Business
from .forms import ProductAddForm,GetOrCreateBusinessForm
from Photo.forms import ProductPhotoAddForm
from Photo.models import ProductPhoto
from History.models import ProductHistory
# from Comment.forms import ProductCommentAddForm
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


# Add product that is already linked to a business through bus_id.
def ProductAddView(request,bus_id):
    #Check to see if the user is authenticated. then returns back to their previous page.
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("Profile:login")
        next_url = reverse("Product:add",kwargs={"bus_id":bus_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)  
    if request.method == 'POST':
        form = ProductAddForm(request.POST,request.FILES)
        imageForm = ProductPhotoAddForm(request.POST,request.FILES)
        if form.is_valid() and imageForm.is_valid():
            product=form.save(commit=False)
            product.business = Business.objects.get(id=bus_id)
            product.author = request.user
            product.save()
            if imageForm.is_bound:
                picForm = imageForm.save(commit=False)
                ProductPhoto.objects.create(product=product, photo= picForm.photo)
            return redirect('Product:detail',product.id)
    form = ProductAddForm()
    imageForm = ProductPhotoAddForm()
    business = Business.objects.get(id=bus_id)
    return render(request,'Product/ProductAddForm.html',{'form':form,'business':business,'imageForm':imageForm})


# shows the detail of the product. 
def ProductDetailView(request,prod_id):
    product = Product.objects.get(id=prod_id)
    total_comments = ProductComment.objects.filter(product=product)
    comments = total_comments.filter(parent__isnull=True)
    replies = total_comments.exclude(parent=None)
    productTags = Tag.objects.filter(products = product)
    context = {'product':product,'comments':comments,"total_comments":total_comments,"productTags":productTags}
    return render(request,'Product/ProductDetail.html',context)

# Edits the product details.
def ProductEditView(request,prod_id):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can edit a product')
        base_url = reverse("Profile:login")
        next_url = reverse("Product:edit",kwargs={"prod_id":prod_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    product = get_object_or_404(Product,id=prod_id)
    try:
        pic = ProductPhoto.objects.get(product=product)
    except ProductPhoto.DoesNotExist:
        pic = ProductPhoto.objects.none()
    if request.method == 'POST':
        imageForm = ProductPhotoAddForm(request.POST,request.FILES)
        form = ProductAddForm(request.POST,request.FILES,instance=product)
        if form.is_valid() and imageForm.is_valid():
            prodForm = form.save(commit=False)
            product.author = request.user
            prodForm.save()
            if imageForm.is_bound:
                if pic:
                    pic.photo=imageForm.cleaned_data['photo']
                    pic.save()
                else:
                    ProductPhoto.objects.create(
                        photo = imageForm.cleaned_data['photo'],
                        product = product
                    )

            return redirect('Product:detail',prod_id)
    form = ProductAddForm(instance=product)
    if pic:
        imageForm = ProductPhotoAddForm(instance=pic)
    else:
        imageForm = ProductPhotoAddForm()
    return render(request,'Product/ProductEditForm.html',{'form':form,'product':product,'imageForm':imageForm})

# List the product of a particular business.
def BusinessProductListView(request,bus_id):
    business = Business.objects.get(id=bus_id)
    products = business.product_set.all().order_by('-date_created')
    return render(request,'Product/BusinessProductGallery.html',{'products':products,'business':business})

# Add a product not already linked to a business - this is done in this function.
def ProductAddGeneralView(request):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("Profile:login")
        next_url = reverse("Product:add-general")
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    if request.method == 'POST':
        ProductAddForm()
        form = ProductAddForm(request.POST,request.FILES)
        form2 = GetOrCreateBusinessForm(request.POST)
        imageForm = ProductPhotoAddForm(request.POST,request.FILES)
        if form.is_valid() and form2.is_valid() and imageForm.is_valid():
            product=form.save(commit=False)
            product.image = imageForm
            # Get of create a business and assign it to product instance.
            try:
                business = Business.objects.get_or_create(name=form2.cleaned_data['business'])[0]
            except:
                business = Business.objects.filter(name=form2.cleaned_data['business']).first()
            
            if not business:
                business = Business.objects.create(name=form2.cleaned_data['business'])
            #Test to see of the business is already selling that product.
            product_in_business = business.product_set.all().filter(name="product.name")
            if product_in_business:
                messages.add_message(request,messages.WARNING,'The product you tried to add is already sold by this business. You can edit this product if it has changed.')
                return redirect("Product:detail",product_in_business.first().id )
            # Assign the business and save the product.
            product.business = business
            product.author = request.user
            product.save()
            # create the ProductPhoto for the product if there's one.
            if imageForm.is_bound:
                ProductPhoto.objects.create(product=product,photo=imageForm.cleaned_data['photo'])
            return redirect('Product:detail',product.id)
    form = ProductAddForm()
    form2 = GetOrCreateBusinessForm()
    imageForm = ProductPhotoAddForm()
    return render(request,'Product/GeneralProductAddForm.html',{'form':form,'form2':form2,'imageForm':imageForm})

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
def ProductListUpload(request,bus_id):
    if not request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,'You need to login before you can add a Product.')
        base_url = reverse("Profile:login")
        next_url = reverse("Product:list-upload",kwargs={"bus_id":bus_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    if request.method == 'POST':
        product_resource = ProductResource()
        dataset = Dataset()
        new_products = request.FILES.get('myfile',False)
        if new_products:
             # Read the uploaded file using BytesIO to handle encoding properly
            file_buffer = io.BytesIO(new_products.read())
            imported_data = dataset.load(file_buffer, format='xlsx', headers=True)
            # Create a list of data to be imported into the dataset.
            author_list, business_list, is_public_list = [], [], []
            author_list.extend(repeat(request.user.id,len(imported_data)))
            business_list.extend(repeat(bus_id,len(imported_data)))
            is_public_list.extend(repeat(1,len(imported_data)))

            # Importing lists into the imported_data set.
            imported_data.append_col(author_list, header='author')
            imported_data.append_col(business_list, header='business')
            imported_data.append_col(is_public_list, header='is_public')
            

            # add the id for  business, author  and is_public ( true or 1) fields for saving.
            result = product_resource.import_data(imported_data,dry_run=True, raise_errors=True) # Test  the data import
            if not result.has_errors():
                product_resource.import_data(imported_data, dry_run=False)
                return redirect("Product:business-list",bus_id)
            # else:
                
            #     print('Error detected')
            #     print(result)
    return render(request,"Product/import_product_list.html")

    

def ProductAutocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term')).order_by('date_created')
        prod_names = list()
        for product in qs:
            prod_names.append(product.name)
        return JsonResponse(prod_names,safe=False)



