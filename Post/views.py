from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, PostLike, PostComment
from .forms import PostForm, PostCommentForm
from Product.models import Product
from Business.models import Business


@login_required
def create_post(request):
    """Create a new post"""
    # Get product or business from query params
    product_id = request.GET.get('product')
    business_id = request.GET.get('business')
    
    product = None
    business = None
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    elif business_id:
        business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('Post:detail', post_id=post.id)
    else:
        initial = {}
        if product:
            initial['product'] = product
        if business:
            initial['business'] = business
        form = PostForm(initial=initial)
    
    context = {
        'form': form,
        'product': product,
        'business': business,
    }
    return render(request, 'Post/create.html', context)


def post_detail(request, post_id):
    """View a single post with its comments"""
    post = get_object_or_404(Post, id=post_id, is_active=True)
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get comments
    comments = post.comments.filter(is_active=True, parent=None)
    
    comment_form = PostCommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'Post/detail.html', context)


def post_feed(request):
    """View feed of all posts"""
    posts = Post.objects.filter(is_active=True).select_related(
        'author', 'product', 'business'
    )
    
    # Filter by type if specified
    filter_type = request.GET.get('type')
    filter_id = request.GET.get('id')
    
    filter_obj = None
    
    if filter_type == 'product':
        posts = posts.filter(product__isnull=False)
        if filter_id:
            posts = posts.filter(product_id=filter_id)
            filter_obj = get_object_or_404(Product, id=filter_id)
            
    elif filter_type == 'business':
        posts = posts.filter(business__isnull=False)
        if filter_id:
            posts = posts.filter(business_id=filter_id)
            filter_obj = get_object_or_404(Business, id=filter_id)
    
    # Pagination
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'filter_obj': filter_obj,
    }
    return render(request, 'Post/feed.html', context)


@login_required
def edit_post(request, post_id):
    """Edit a post"""
    post = get_object_or_404(Post, id=post_id, author=request.user, is_active=True)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('Post:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'Post/edit.html', context)


@login_required
def delete_post(request, post_id):
    """Delete a post (soft delete)"""
    post = get_object_or_404(Post, id=post_id, author=request.user, is_active=True)
    
    if request.method == 'POST':
        post.is_active = False
        post.save()
        messages.success(request, 'Post deleted successfully!')
        return redirect('Home:home')
    
    context = {'post': post}
    return render(request, 'Post/delete_confirm.html', context)


@login_required
def toggle_like(request, post_id):
    """Toggle like on a post (HTMX endpoint)"""
    post = get_object_or_404(Post, id=post_id, is_active=True)
    
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # Toggle the like
        like.is_active = not like.is_active
        like.save()
    
    # Return updated like button HTML
    context = {
        'post': post,
        'user': request.user,
    }
    return render(request, 'Post/partials/like_button.html', context)


@login_required
def add_comment(request, post_id):
    """Add a comment to a post (HTMX endpoint)"""
    post = get_object_or_404(Post, id=post_id, is_active=True)
    
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            
            # Handle parent comment for replies
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(PostComment, id=parent_id)
            
            comment.save()
            
            # Return the new comment HTML
            context = {
                'comment': comment,
                'post': post,
            }
            return render(request, 'Post/partials/comment.html', context)
    
    return HttpResponse(status=400)


def user_posts(request, username):
    """View all posts by a specific user"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    
    posts = Post.objects.filter(
        author=user, 
        is_active=True
    ).select_related('product', 'business')
    
    # Pagination
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'page_obj': page_obj,
    }
    return render(request, 'Post/user_posts.html', context)
