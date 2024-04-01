from django.shortcuts import render,redirect
from Product.models import Product
from .models import ProductSubscription
from django.contrib.auth.models import User
# Create your views here.

def FollowView(request,prod_id):
    if not request.user.is_authenticated:
        return redirect('Profile:login')
    product1 = Product.objects.get(id=prod_id)
    # Check to see if there is already a prior subscription.
    test = ProductSubscription.objects.filter(user=request.user).filter(product=product1)
    if test.exists():
        return redirect('Product:detail',prod_id)

    ProductSubscription.objects.create(user=request.user,product=product1)
    return redirect('Product:detail',prod_id)


def UnfollowView(request,prod_id):
    mySub = ProductSubscription.objects.filter(user=request.user,product=Product.objects.get(id=prod_id))
    mySub.first.delete()
    return redirect('Product:detail',prod_id)



def SubscriptionsView(request):
    if not request.user.is_authenticated:
        return redirect('Profile:login')
    my_subs = ProductSubscription.objects.filter(user=request.user)
    all_products =list()
    for sub in my_subs:
        all_products.append(sub.product)
    return render(request,'Follow/my_subscriptions.html',{'products':all_products})
