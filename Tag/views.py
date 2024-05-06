from django.shortcuts import render,redirect
from django.db.models import Count,Min,Max,Sum,Avg
from Product.models import Product
from .models import Tag
from django.http import JsonResponse


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
    if 'term' in request.GET:
        qs = Tag.objects.filter(name__icontains=request.GET.get('term'))
        tag_names = list()
        for tag in qs:
            tag_names.append(tag.name)
        return JsonResponse(tag_names,safe=False)

def TagProductsView(request,tag_id):
    tag = Tag.objects.get(id=tag_id)
    products = tag.products.all()
    TagSumm = products.aggregate(Max('price'),Min('price'),Avg('price'))
    return render(request,'Tag/tag_products.html',{'products':products,'tag':tag, 'summary':TagSumm})
    