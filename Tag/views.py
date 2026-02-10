from django.shortcuts import render,redirect
from django.db.models import Count,Min,Max,Sum,Avg, Q
from Product.models import Product
from .models import Tag
from django.http import JsonResponse, HttpResponse

def AddTagView(request,prod_id):
    t = request.POST.get("tag")
    product = Product.objects.get(id=prod_id)
    try:
        tag = Tag.objects.get(name=t)
    except Tag.DoesNotExist:
        tag = Tag(name=t)
        tag.save()
    tag.products.add(product)
    return redirect('Product:detail',prod_id)

def TagAutocomplete(request):
    """Legacy JSON autocomplete"""
    if 'term' in request.GET:
        qs = Tag.objects.filter(name__icontains=request.GET.get('term'))
        tag_names = list()
        for tag in qs:
            tag_names.append(tag.name)
        return JsonResponse(tag_names,safe=False)

def TagAutocompleteHtmx(request):
    """HTMX autocomplete that returns HTML partial"""
    query = request.GET.get('tags_input', '')
    
    # Get the last comma-separated value
    if ',' in query:
        search_term = query.split(',')[-1].strip()
    else:
        search_term = query.strip()
        
    if len(search_term) >= 3:
        tags = Tag.objects.filter(name__icontains=search_term)[:10]
    else:
        tags = []
        
    return render(request, 'Tag/partials/tag_suggestions.html', {'tags': tags})

def RenderTagChip(request):
    """Renders a bootstrap badge for a tag"""
    tag_name = request.GET.get('tag', '').strip()
    if not tag_name:
        return HttpResponse('')
        
    # Check if exists to style differently if needed (user requested "let user know... same for tag that already exist")
    exists = Tag.objects.filter(name__iexact=tag_name).exists()
    
    context = {
        'tag_name': tag_name,
        'exists': exists
    }
    return render(request, 'Tag/partials/tag_chip.html', context)

def TagProductsView(request,tag_id,product_id=None):
    tag = Tag.objects.get(id=tag_id)
    products = tag.products.all()
    TagSumm = products.aggregate(Max('price'),Min('price'),Avg('price'))
    
    # Identify the current product
    current_product = None
    if product_id:
        try:
            current_product = products.get(id=product_id)
        except:
            pass
    
    # Prepare data for the scatter chart
    product_data = []
    for i, product in enumerate(products, start=1):
        is_current = product == current_product
        product_data.append({
            'index': i,
            'name': product.name,
            'price': float(product.price),
            'business': product.business.name if product.business else 'Unknown',
            'is_current': 'true' if is_current else 'false'
        })
    
    return render(request,'Tag/tag_products.html',{
        'products':products,
        'tag':tag, 
        'summary':TagSumm,
        'product_data': product_data,
        'current_product': current_product
    })