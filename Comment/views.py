from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views import View
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlencode

from Product.models import Product
from Business.models import Business
from Information.models import Info
from .models import ProductComment, BusinessComment, InfoComment
from .forms import ProductCommentForm, BusinessCommentForm, InfoCommentForm
from Tag.models import Tag

# --- Legacy function-based views (for backward compatibility) ---
def ProductCommentView(request, prod_id):
    try:
        # Import models locally
        from .models import ProductComment
        from Product.models import Product
    except ImportError as e:
        print(f"Import error in ProductCommentView: {e}")
        return HttpResponse('Model import error', status=500)

    if not request.user.is_authenticated:
        if request.htmx:
            return HttpResponse(
                'Please <a href="' + reverse("account_login") + '?next=' + reverse("Product:detail", kwargs={"prod_id": prod_id}) + '">login</a> to post comments.'
            )
        messages.warning(request, 'Sorry you need to login first')
        base_url = reverse("account_login")
        next_url = reverse("Product:detail", kwargs={"prod_id": prod_id})
        next = urlencode({"next": next_url})
        url = '{}?{}'.format(base_url, next)
        return redirect(url)

    if request.method == "POST":
        try:
            body = request.POST.get('comment')
            product = get_object_or_404(Product, id=prod_id)
            parent_comment_id = request.POST.get('parentComment')
            if parent_comment_id == 'none':
                comment = ProductComment.objects.create(body=body, user=request.user, product=product)
            else:
                parent_comment = get_object_or_404(ProductComment, id=parent_comment_id)
                comment = ProductComment.objects.create(body=body, user=request.user, product=product, parent=parent_comment)
            if request.headers.get('HX-Request'):
                if parent_comment_id != 'none':
                    html = f'<div id="comment-{comment.id}">' + render_to_string('Comment/comment_item.html', {'comment': comment, 'request': request, 'product': product}) + '</div>'
                else:
                    html = render_to_string('Comment/comment_item.html', {'comment': comment, 'request': request, 'product': product})
                return HttpResponse(html)
            return redirect('Product:detail', prod_id=prod_id)
        except Exception as e:
            if request.headers.get('HX-Request'):
                return HttpResponse(f"Error: {str(e)}", status=400)
            messages.error(request, f"Error: {str(e)}")
            return redirect('Product:detail', prod_id=prod_id)

    if request.method == "GET" and request.headers.get('HX-Request'):
        try:
            update_count_id = request.GET.get('update_count')
            if update_count_id:
                comment = get_object_or_404(ProductComment, id=update_count_id)
                return HttpResponse(comment.check_replies)
        except Exception as e:
            return HttpResponse("", status=400)

    product = get_object_or_404(Product, id=prod_id)
    total_comments = ProductComment.objects.filter(product=product)
    comments = total_comments.filter(parent__isnull=True).order_by('-date')
    replies = total_comments.exclude(parent=None)
    product_tags = Tag.objects.filter(products=product)
    context = {
        'product': product,
        'comments': comments,
        "total_comments": total_comments,
        "productTags": product_tags
    }
    return render(request, "Product/ProductDetail.html", context)

def LoadMoreComments(request, prod_id):
    try:
        # Import models locally
        from .models import ProductComment
        from Product.models import Product
    except ImportError as e:
        print(f"Import error in LoadMoreComments: {e}")
        return HttpResponse('Model import error', status=500)

    if not request.user.is_authenticated:
        return HttpResponse('')
    page = request.GET.get('page', 1)
    product = Product.objects.get(id=prod_id)
    comments = ProductComment.objects.filter(
        product=product,
        parent__isnull=True
    ).order_by('-date')
    paginator = Paginator(comments, 10)
    comments_page = paginator.get_page(page)
    if not comments_page.has_next():
        return HttpResponse('')
    html = render_to_string('Comment/comment_template.html', {
        'comments': comments_page,
        'request': request,
        'product': product
    })
    return HttpResponse(html)

def DeleteProductCommentView(request, com_id):
    try:
        # Import models locally
        from .models import ProductComment
        from Product.models import Product
    except ImportError as e:
        print(f"Import error in DeleteProductCommentView: {e}")
        return HttpResponse('Model import error', status=500)

    comment = ProductComment.objects.get(id=com_id)
    prod_id = comment.product.id
    if not request.user.is_authenticated:
        messages.warning(request, 'Sorry you need to login first')
        base_url = reverse("account_login")
        next_url = reverse("Product:detail", kwargs={"prod_id": prod_id})
        next = urlencode({"next": next_url})
        url = '{}?{}'.format(base_url, next)
        return redirect(url)
    if request.user == comment.user:
        replies = comment.replies.all()
        for reply in replies:
            reply.delete()
        comment.delete()
        if request.headers.get('HX-Request'):
            return HttpResponse('')
    return redirect('Product:detail', prod_id=prod_id)

def SeekCommentView(request, com_id):
    try:
        # Import models locally
        from .models import ProductComment
        from Product.models import Product
    except ImportError as e:
        print(f"Import error in SeekCommentView: {e}")
        return HttpResponse('Model import error', status=500)

    comment = ProductComment.objects.get(id=com_id)
    product = comment.product
    data_dict = {"key": com_id, "body": comment.body}
    total_comments = ProductComment.objects.filter(product=product)
    comments = total_comments.filter(parent__isnull=True).order_by('-date')
    replies = total_comments.exclude(parent=None)
    product_tags = Tag.objects.filter(products=product)
    context = {
        'jsData': data_dict,
        'product': product,
        'comments': comments,
        "total_comments": total_comments,
        "productTags": product_tags
    }
    return render(request, 'Product/ProductDetail.html', context)

# --- New generic class-based comment views ---
class CommentListView(View):
    def get(self, request):
        try:
            content_type = request.GET.get('content_type')
            object_id = request.GET.get('object_id')
            page = request.GET.get('page', 1)

            # Import models locally to avoid import issues
            try:
                from .models import ProductComment, BusinessComment, InfoComment
            except ImportError as e:
                print(f"Import error in CommentListView: {e}")
                return HttpResponse('Model import error', status=500)

            model_map = {
                'product': ProductComment,
                'business': BusinessComment,
                'info': InfoComment,
            }
            model = model_map.get(content_type)
            if not model:
                return HttpResponse('Invalid content type', status=400)

            # Validate object_id
            try:
                object_id = int(object_id)
            except (ValueError, TypeError):
                return HttpResponse('Invalid object id', status=400)

            # Validate page
            try:
                page = int(page)
            except (ValueError, TypeError):
                page = 1

            # Query comments
            try:
                comments = model.objects.filter(
                    **{f'{content_type}__id': object_id},
                    parent__isnull=True,
                    is_active=True
                ).order_by('-created_at')
                paginator = Paginator(comments, 10)
                page_obj = paginator.get_page(page)
            except Exception as query_error:
                print(f"Query error in CommentListView: {query_error}")
                return HttpResponse('Database query error', status=500)

            # Check if there are more pages
            has_next = page_obj.has_next()
            next_page = page_obj.next_page_number() if has_next else None

            context = {
                'comments': page_obj,
                'request': request,
                'has_next': has_next,
                'next_page': next_page,
            }

            try:
                html = render_to_string('Comment/comment_list.html', context, request=request)
                return HttpResponse(html)
            except Exception as render_error:
                print(f"Template render error in CommentListView: {render_error}")
                return HttpResponse('Template render error', status=500)

        except Exception as e:
            # Log the error and return a user-friendly message
            import traceback
            print(f"Error in CommentListView: {str(e)}")
            print(traceback.format_exc())
            return HttpResponse('Error loading comments', status=500)

class CommentCreateView(View):
    def post(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponse(
                'Please <a href="' + reverse("account_login") + '?next=' + request.path + '">login</a> to post comments.',
                status=401
            )

        try:
            content_type = request.POST.get('content_type')
            object_id = request.POST.get('object_id')
            parent_id = request.POST.get('parent_id')
            body = request.POST.get('body', '').strip()

            # Validate body length
            if not body or len(body) > 500:
                return HttpResponse('Invalid comment body', status=400)

            # Import models locally
            try:
                from .models import ProductComment, BusinessComment, InfoComment
                from Product.models import Product
                from Business.models import Business
                from Information.models import Info
            except ImportError as e:
                print(f"Import error in CommentCreateView: {e}")
                return HttpResponse('Model import error', status=500)

            model_map = {
                'product': (ProductComment, 'product', Product),
                'business': (BusinessComment, 'business', Business),
                'info': (InfoComment, 'info', Info),
            }
            model_tuple = model_map.get(content_type)
            if not model_tuple:
                return HttpResponse('Invalid content type', status=400)

            model, fk_name, fk_model = model_tuple

            parent = None
            if parent_id:
                try:
                    parent = model.objects.get(id=parent_id, is_active=True)
                except model.DoesNotExist:
                    parent = None

            # Create the comment instance manually
            comment = model()
            comment.user = request.user

            # If this is a reply to another reply, add @username prefix
            if parent and parent.parent:
                # This is a reply to a reply, add @parent_user
                parent_user = parent.user
                body = f"@{parent_user.username} {body}"

            comment.body = body
            comment.is_active = True
            comment.parent = parent

            try:
                instance = fk_model.objects.get(id=int(object_id))
            except (fk_model.DoesNotExist, ValueError, TypeError):
                return HttpResponse('Invalid object id', status=400)

            setattr(comment, fk_name, instance)
            comment.save()

            html = render_to_string('Comment/comment_item.html', {'comment': comment, 'request': request}, request=request)
            response_html = f"""
            {html}
            <script>
                // Expand the parent comment's replies container to show the new reply
                const parentRepliesContainer = document.getElementById('replies-{parent_id}');
                if (parentRepliesContainer && !parentRepliesContainer.classList.contains('expanded')) {{
                    parentRepliesContainer.classList.add('expanded');
                }}
            </script>
            """
            return HttpResponse(response_html)

        except Exception as e:
            return HttpResponse(f'Server error: {str(e)}', status=500)

class CommentDeleteView(View):
    def post(self, request, pk):
        try:
            # Import models locally
            try:
                from .models import ProductComment, BusinessComment, InfoComment
            except ImportError as e:
                print(f"Import error in CommentDeleteView: {e}")
                return HttpResponse('Model import error', status=500)

            for model in (ProductComment, BusinessComment, InfoComment):
                try:
                    comment = model.objects.get(pk=pk, is_active=True)
                    if request.user == comment.user or request.user.is_superuser:
                        # Soft delete the comment and all its replies
                        comment.is_active = False
                        comment.save()

                        # Also soft delete all replies to this comment
                        replies = model.objects.filter(parent=comment, is_active=True)
                        replies.update(is_active=False)

                        return HttpResponse('')
                except model.DoesNotExist:
                    continue
            return HttpResponse('Not found or not allowed', status=404)
        except Exception as e:
            print(f"Error in CommentDeleteView: {str(e)}")
            return HttpResponse('Error deleting comment', status=500) 