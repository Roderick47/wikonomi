from django.shortcuts import render,redirect
from Product.models import Product
from .models import ProductComment
from Tag.models import Tag

from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlencode
from json import dumps




def ProductCommentView(request,prod_id):
    if not request.user.is_authenticated:
        messages.warning(request,'Sorry you need to login first')
        base_url = reverse("Profile:login")
        next_url = reverse("Product:detail",kwargs={"prod_id":prod_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    if request.method == "POST":
        body = request.POST.get('comment')
        product = Product.objects.get(id=prod_id)
        parentCommentId = request.POST.get('parentComment')
        # if there is no parent comment create a new ProductComment else make a reply to a comment.
        if parentCommentId =='none':
            comment = ProductComment.objects.create(body=body,user=request.user,product=product)
            jsData = dumps({"commentID":"{{comment.id}}-{{comment.body}}"})
        else:
            parentComment = ProductComment.objects.get(id=parentCommentId)
            ProductComment.objects.create(body=body,user=request.user,product=product,parent=parentComment)
            jsData = dumps({ "commentID" : "{{parentComment.id}}-{{parentComment.body}}" })

#    product = Product.objects.get(id=prod_id)
    total_comments = ProductComment.objects.filter(product=product)
    comments = total_comments.filter(parent__isnull=True)
    replies = total_comments.exclude(parent=None)
    productTags = Tag.objects.filter(products = product)
        
    context = {"data":jsData,'product':product,'comments':comments,"total_comments":total_comments,"productTags":productTags}
    
    return render(request,"Product/ProductDetail.html",context)


# deletes the ProductComment object.
def DeleteProductCommentView(request,com_id):
    comment = ProductComment.objects.get(id=com_id)
    prod_id= comment.product.id
    if not request.user.is_authenticated:
        messages.warning(request,'Sorry you need to login first')
        base_url = reverse("Profile:login")
        next_url = reverse("Product:detail",kwargs={"prod_id":prod_id})
        next = urlencode({"next":next_url})
        url = '{}?{}'.format(base_url,next)
        return redirect(url)
    # Delete all the replies to the comment.
    replies = comment.replies.all()
    for reply in replies:
        reply.delete()
    comment.delete()
    return redirect('Product:detail',prod_id)


def SeekCommentView(request,com_id):
    # select the individual comment
    comment = ProductComment.objects.get(id=com_id)
    product = comment.product
    dataDict = {"key":com_id,"body":comment.body}
    jsData = dumps(dataDict)

    # render all the other context information for the page.
    total_comments = ProductComment.objects.filter(product=product)
    comments = total_comments.filter(parent__isnull=True)
    replies = total_comments.exclude(parent=None)
    productTags = Tag.objects.filter(products = product)

    context = {'jsData':jsData,'product':product,'comments':comments,"total_comments":total_comments,
        "productTags":productTags}

    return render(request,'Product/ProductDetail.html',context)
