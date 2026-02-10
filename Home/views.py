from django.shortcuts import render
from Product.models import Product
import datetime


from Business.models import Business
from Post.models import Post

from django.utils import timezone

from QA.models import Question
from HowTo.models import HowTo

def HomeView(request):
    # Get all posts
    posts = Post.objects.filter(is_active=True)

    # Get all questions
    questions = Question.objects.all()
    
    # Get all products and businesses (including updated ones)
    products = Product.objects.all()
    businesses = Business.objects.all()
    howtos = HowTo.objects.filter(is_public=True)

    # Label items for template rendering and normalize date for sorting
    feed_items = []
    
    for post in posts:
        post.item_type = 'post'
        post.sorting_date = post.created_at
        feed_items.append(post)

    for question in questions:
        question.item_type = 'question'
        question.sorting_date = question.created_at
        feed_items.append(question)
        
    for product in products:
        product.item_type = 'product'
        product.sorting_date = product.date_updated
        # Determine verb based on update time vs creation time
        if product.date_updated > product.date_created + datetime.timedelta(minutes=5):
            product.verb = 'updated a product'
        else:
            product.verb = 'listed a new product'
        feed_items.append(product)
        
    for business in businesses:
        business.item_type = 'business'
        business.sorting_date = business.date_updated
        if business.date_updated > business.date_created + datetime.timedelta(minutes=5):
            business.verb = 'updated a business profile'
        else:
            business.verb = 'registered a new business'
        feed_items.append(business)

    for howto in howtos:
        howto.item_type = 'howto'
        howto.sorting_date = howto.updated_at
        if howto.updated_at > howto.created_at + datetime.timedelta(minutes=5):
            howto.verb = 'updated a guide'
            howto.feed_author = howto.last_editor or howto.author
        else:
            howto.verb = 'published a new guide'
            howto.feed_author = howto.author
        feed_items.append(howto)
    
    # Sort by date descending
    feed_items.sort(key=lambda x: x.sorting_date, reverse=True)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(feed_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'feed_items': page_obj}
    
    if request.headers.get('HX-Request'):
        return render(request, 'Home/partials/feed_chunk.html', context)
    
    return render(request, 'Home/home.html', context)

def AboutView(request):
    return render(request,'Home/about.html')
