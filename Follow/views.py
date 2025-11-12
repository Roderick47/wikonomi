from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from Product.models import Product
from .models import ProductSubscription
from History.models import ProductHistory
from django.contrib.auth.models import User
from django.db.models import Q
from collections import defaultdict
import json
# Create your views here.

def FollowProductView(request,prod_id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    product1 = Product.objects.get(id=prod_id)
    # Check to see if there is already a prior subscription.
    test = ProductSubscription.objects.filter(user=request.user).filter(product=product1)
    if test.exists():
        return redirect('Product:detail',prod_id)

    ProductSubscription.objects.create(user=request.user,product=product1)
    return redirect('Product:detail',prod_id)


def UnfollowView(request,prod_id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    mySub = ProductSubscription.objects.filter(user=request.user, product=Product.objects.get(id=prod_id))
    if mySub.exists():
        mySub.first().delete()
    return redirect('Product:detail',prod_id)



def SubscriptionsView(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    my_subs = ProductSubscription.objects.filter(user=request.user)
    all_products =list()
    for sub in my_subs:
        all_products.append(sub.product)
    return render(request,'Follow/my_subscriptions.html',{'products':all_products})


def WatchlistView(request):
    """Display tracked products with their last prices from history"""
    if not request.user.is_authenticated:
        return redirect('account_login')
    
    # Get user's tracked products
    subscriptions = ProductSubscription.objects.filter(user=request.user).select_related('product', 'product__business')
    
    # Prepare product data with last prices
    watchlist_items = []
    products_by_business = defaultdict(list)
    
    for subscription in subscriptions:
        product = subscription.product
        
        watchlist_item = {
            'product': product,
            'subscription': subscription,
            'has_history': product.has_price_history()
        }
        
        watchlist_items.append(watchlist_item)
        
        # Group by business
        if product.business:
            business_name = product.business.name
            products_by_business[business_name].append(watchlist_item)
        else:
            # Group products without business under "Other"
            products_by_business["Other"].append(watchlist_item)
    
    return render(request, 'Follow/watchlist.html', {
        'watchlist_items': watchlist_items,
        'total_tracked': len(watchlist_items),
        'products_by_business': dict(products_by_business)
    })


@csrf_exempt
@require_http_methods(['POST'])
@login_required(login_url='/accounts/login/')
def api_toggle_watchlist(request, product_id):
    """API endpoint to add/remove product from watchlist"""
    try:
        product = get_object_or_404(Product, id=product_id)
        subscription = ProductSubscription.objects.filter(user=request.user, product=product).first()
        
        if subscription:
            subscription.delete()
            return JsonResponse({
                'status': 'success',
                'action': 'removed',
                'message': 'Product removed from watchlist'
            })
        else:
            ProductSubscription.objects.create(user=request.user, product=product)
            return JsonResponse({
                'status': 'success',
                'action': 'added',
                'message': 'Product added to watchlist'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
