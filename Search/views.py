from django.shortcuts import render,redirect
from django.db.models import Q
from Product.models import Product
from Business.models import Business
from Post.models import Post
from QA.models import Question
# from .forms import ChooseSpecForm
from .models import pager,combine_query_sets
from HowTo.models import HowTo
from django.http import JsonResponse



def SearchView(request):
    query = request.GET.get('q','')
    search_type = request.GET.get('type', '')  # Get optional type filter
    
    # Initialize all result lists
    products_results_list = Product.objects.none()
    business_results_list = Business.objects.none()
    question_results_list = Question.objects.none()
    howto_results_list = HowTo.objects.none()
    post_results_list = Post.objects.none()
    
    # Search based on type filter or search all if no type specified
    if not search_type or search_type == 'product':
        products_results_list = Product.objects.filter(
            Q(name__icontains=query)|Q(description__icontains=query)|Q(tags__name__icontains=query)
            ).select_related('business').distinct()
        products_results_list = products_results_list.order_by('price')
    
    if not search_type or search_type == 'business':
        business_results_list = Business.objects.filter(
            Q(name__icontains=query)|Q(description__icontains=query)
            ).distinct()
        business_results_list = business_results_list.order_by('name')
    
    if not search_type or search_type == 'question' or search_type == 'knowledge':
        question_results_list = Question.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()

    if not search_type or search_type == 'knowledge':
        howto_results_list = HowTo.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_public=True
        ).distinct()
    
    if not search_type or search_type == 'post':
        post_results_list = Post.objects.filter(
            Q(body__icontains=query),
            is_active=True
        ).select_related('author', 'product', 'business').distinct()
        post_results_list = post_results_list.order_by('-created_at')
    
    # Paginate results
    products_results = pager(request, products_results_list, 6)
    business_results = pager(request, business_results_list, 6)
    question_results = pager(request, question_results_list, 6)
    howto_results = pager(request, howto_results_list, 6)
    post_results = pager(request, post_results_list, 6)

    return render(request,'Search/results.html',{
        'products_results_list':products_results_list,
        'products_results':products_results,
        'query':query,
        'business_results_list':business_results_list,
        'business_results':business_results,
        'question_results_list': question_results_list,
        'question_results': question_results,
        'howto_results_list': howto_results_list,
        'howto_results': howto_results,
        'post_results_list': post_results_list,
        'post_results': post_results,
        'search_type': search_type,
    })


def BusinessSearchView(request,query):
    results_list = Business.objects.filter(
        Q(name__icontains=query)|Q(description__icontains=query)
        )
    results_list = results_list.order_by('name')
    results = pager(request,results_list,12)
    return render(request,'Search/business_results.html',{'results_list':results_list,'businesses':results,'query':query})

# Renders the advanced Search page.
def AdvancedSearchView(request):
    SpecForm=ChooseSpecForm()
    return render(request,'Search/advanced_search_form.html',{'SpecForm':SpecForm})


def AdvancedSearchResultsView(request):
    price = request.GET.get('price','')
    mileage = request.GET.get('mileage','')
    car_type = request.GET.get('car_type','')
    brand = request.GET.get('brand','')
    # Need to filter out results so that sold vehicles do not appear in the search results. To do.
    if price or mileage or car_type or brand :
        results_list = Vehicle.objects.all()
        if mileage:
            results_list = results_list.filter(vehiclespec__mileage__lte=mileage).filter()
        if brand:
            results_list = results_list.filter(brand__name=brand)
        if car_type:
            results_list = results_list.filter(vehicle_type__name=car_type)
        if price:
            results_list = results_list.filter(price__lte=price)
        results_list = results_list.order_by('price')
    else:    
        results_list = Vehicle.objects.none()
    results = pager(request,results_list,12)
    context = {'results_list':results_list,'vehicles':results,"price":price,
        "car_type":car_type,"brand":brand,"mileage":mileage}
    return render(request,'Search/advanced_results.html',context)


def SearchAutocomplete(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        budget_id = request.GET.get('budget_id')
        
        if len(query) >= 2:  # Only search if query is 2+ characters
            qs = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(business__name__icontains=query)
            )
            
            # Exclude products already in the budget if budget_id is provided
            if budget_id:
                from Budget.models import Budget
                try:
                    budget = Budget.objects.get(id=budget_id)
                    qs = qs.exclude(id__in=budget.products.values_list('id', flat=True))
                except (Budget.DoesNotExist, ValueError):
                    pass
            
            qs = qs.select_related('business')[:10]  # Limit to 10 results
            
            return render(request, 'Search/autocomplete_suggestions.html', {
                'products': qs,
                'query': query,
                'budget_id': budget_id
            })
    return render(request, 'Search/autocomplete_suggestions.html', {'products': [], 'query': ''})



