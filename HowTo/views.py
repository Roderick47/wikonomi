from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.db import models
from .models import HowTo, HowToStep, HowToHistory
from .forms import HowToForm, HowToStepForm
from .utils import create_howto_snapshot
from Business.models import Business
from Product.models import Product
from QA.models import Question
from django.forms import modelformset_factory
from django.urls import reverse

@login_required
def HowToCreateView(request):
    bus_id = request.GET.get('business')
    prod_id = request.GET.get('product')
    q_id = request.GET.get('question')
    
    business = None
    product = None
    question = None
    
    if bus_id:
        business = get_object_or_404(Business, id=bus_id)
        if not business.is_public and business.author != request.user:
            return HttpResponseForbidden("You cannot add documentation to a private business.")
    
    if prod_id:
        product = get_object_or_404(Product, id=prod_id)
        if not product.business.is_public and product.business.author != request.user:
            return HttpResponseForbidden("You cannot add documentation to a private product.")
    
    if q_id:
        question = get_object_or_404(Question, id=q_id)

    if request.method == 'POST':
        form = HowToForm(request.POST)
        if form.is_valid():
            howto = form.save(commit=False)
            howto.author = request.user
            
            # Inheritance of visibility
            if business:
                howto.business = business
                howto.is_public = business.is_public
            if product:
                howto.product = product
                howto.is_public = product.business.is_public
            if question:
                howto.origin_question = question
            
            howto.save()
            
            # Handle steps
            step_titles = request.POST.getlist('step_title[]')
            step_contents = request.POST.getlist('step_content[]')
            step_images = request.FILES.getlist('step_image[]')
            
            for i, (title, content) in enumerate(zip(step_titles, step_contents)):
                if content:
                    step = HowToStep(
                        how_to=howto,
                        title=title,
                        content=content,
                        order=i+1
                    )
                    # Note: Handle list of files specifically if needed, 
                    # but usually better with individual form logic for simplicity in MVP.
                    if i < len(step_images):
                        step.image = step_images[i]
                    step.save()
            
            # Create initial snapshot
            create_howto_snapshot(howto, request.user, summary="Initial version")
            
            messages.success(request, "Documentation created successfully!")
            return redirect('HowTo:detail', how_id=howto.id)
    else:
        initial = {}
        if business: initial['business'] = business
        if product: initial['product'] = product
        
        form = HowToForm(initial=initial)
        if question:
            form.fields['title'].initial = f"Guide: {question.title}"
            form.fields['description'].initial = question.body

    return render(request, 'HowTo/howto_form.html', {
        'form': form,
        'business': business,
        'product': product,
        'question': question
    })

def HowToDetailView(request, how_id):
    howto = get_object_or_404(HowTo, id=how_id)
    
    # Privacy check
    if not howto.is_public:
        is_authorized = False
        if request.user.is_authenticated:
            if howto.author == request.user:
                is_authorized = True
            elif howto.business and howto.business.author == request.user:
                is_authorized = True
            elif howto.product and howto.product.business.author == request.user:
                is_authorized = True
        
        if not is_authorized:
            return HttpResponseForbidden("This is private documentation.")

    # Edit permissions check
    can_edit = False
    if request.user.is_authenticated:
        if howto.business:
            if howto.business.is_public or howto.business.author == request.user:
                can_edit = True
        elif howto.product:
            if howto.product.business.is_public or howto.product.business.author == request.user:
                can_edit = True
        else:
            can_edit = True # Community guides

    # View counting logic
    howto.views_count += 1
    howto.save(update_fields=['views_count'])
    
    # Prepare steps with their top question
    # Get all steps and annotate each with its top-voted question
    steps_with_questions = []
    for step in howto.steps.all():
        # Get the top voted question for this step
        # Using annotations to calculate total likes across all answers
        top_question = step.questions.annotate(
            total_votes=models.Count('answers__likes')
        ).order_by('-total_votes', '-created_at').first()
        
        steps_with_questions.append({
            'step': step,
            'top_question': top_question,
            'questions_count': step.questions.count()
        })
    
    return render(request, 'HowTo/howto_detail.html', {
        'howto': howto,
        'can_edit': can_edit,
        'steps_with_questions': steps_with_questions,
        'canonical_url': request.build_absolute_uri(
            reverse('HowTo:detail', kwargs={'how_id': howto.id})
        ),
    })

@login_required
def HowToEditView(request, how_id):
    howto = get_object_or_404(HowTo, id=how_id)
    
    # Permission check for editing
    is_authorized = False
    if howto.business:
        if howto.business.is_public or howto.business.author == request.user:
            is_authorized = True
    elif howto.product:
        if howto.product.business.is_public or howto.product.business.author == request.user:
            is_authorized = True
    else:
        is_authorized = True
        
    if not is_authorized:
        return HttpResponseForbidden("You do not have permission to edit this guide.")

    if request.method == 'POST':
        form = HowToForm(request.POST, instance=howto)
        if form.is_valid():
            howto = form.save(commit=False)
            howto.last_editor = request.user
            howto.version += 1
            howto.save()
            
            # Record current steps for snapshot before updating them
            # (Though it's better to snapshot AFTER saving new state for the new version number)
            
            # Clear old steps and add new ones (Simple approach for version control MVP)
            # In a more advanced system, we'd sync them.
            old_steps = list(howto.steps.all())
            
            step_titles = request.POST.getlist('step_title[]')
            step_contents = request.POST.getlist('step_content[]')
            step_images = request.FILES.getlist('step_image[]')
            
            # Temporary storage to rebuild
            new_steps = []
            for i, (title, content) in enumerate(zip(step_titles, step_contents)):
                if content:
                    step = HowToStep(
                        how_to=howto,
                        title=title,
                        content=content,
                        order=i+1
                    )
                    if i < len(step_images):
                        step.image = step_images[i]
                    elif i < len(old_steps) and old_steps[i].image:
                        # Keep existing image if no new one uploaded
                        step.image = old_steps[i].image
                    new_steps.append(step)
            
            # Atomically update
            howto.steps.all().delete()
            for s in new_steps: s.save()
            
            # Create snapshot of the NEW state
            summary = request.POST.get('change_summary', f"Updated to version {howto.version}")
            create_howto_snapshot(howto, request.user, summary=summary)
            
            messages.success(request, f"Guide updated to version {howto.version}!")
            return redirect('HowTo:detail', how_id=howto.id)
    else:
        form = HowToForm(instance=howto)

    return render(request, 'HowTo/howto_form.html', {
        'form': form,
        'howto': howto,
        'is_edit': True,
        'business': howto.business,
        'product': howto.product
    })

def HowToHistoryView(request, how_id):
    howto = get_object_or_404(HowTo, id=how_id)
    if not howto.is_public:
        is_authorized = request.user.is_authenticated and (
            howto.author == request.user
            or (howto.business and howto.business.author == request.user)
            or (howto.product and howto.product.business.author == request.user)
        )
        if not is_authorized:
            return HttpResponseForbidden("This is private documentation.")

    history = howto.history.all().order_by('-version')
    response = render(request, 'HowTo/howto_history.html', {
        'howto': howto,
        'history': history,
        'canonical_url': request.build_absolute_uri(
            reverse('HowTo:detail', kwargs={'how_id': howto.id})
        ),
    })
    # Search engines must not index snapshots or split ranking signals away
    # from the current guide. The HTTP header also covers non-HTML crawlers.
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response

@login_required
def HowToOfficialToggle(request, how_id):
    howto = get_object_or_404(HowTo, id=how_id)
    
    # Permission check: Only business owner can mark as official
    is_owner = False
    if howto.business and howto.business.author == request.user:
        is_owner = True
    elif howto.product and howto.product.business.author == request.user:
        is_owner = True
        
    if not is_owner:
        return HttpResponseForbidden("Only the business owner can designate official documentation.")
    
    howto.is_official = not howto.is_official
    howto.save()
    
    status = "official" if howto.is_official else "unofficial"
    messages.success(request, f"Documentation marked as {status}.")
    return redirect('HowTo:detail', how_id=howto.id)

@login_required
def HowToListView(request):
    # Filter public ones + private ones authored by user
    how_tos = HowTo.objects.filter(is_public=True) | HowTo.objects.filter(author=request.user)
    return render(request, 'HowTo/howto_list.html', {'how_tos': how_tos.distinct()})

def ProductGuidesView(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Privacy check for product
    if not product.business.is_public and product.business.author != request.user:
        return HttpResponseForbidden("You cannot view documentation for a private product.")
    
    # Get guides for this product (public + user's private ones)
    how_tos = HowTo.objects.filter(product=product).filter(
        models.Q(is_public=True) | models.Q(author=request.user)
    ).distinct().order_by('-created_at')
    
    return render(request, 'HowTo/product_guides.html', {
        'product': product,
        'how_tos': how_tos
    })

def BusinessGuidesView(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    
    # Privacy check for business
    if not business.is_public and business.author != request.user:
        return HttpResponseForbidden("You cannot view documentation for a private business.")
    
    # Get guides for this business (public + user's private ones)
    how_tos = HowTo.objects.filter(business=business).filter(
        models.Q(is_public=True) | models.Q(author=request.user)
    ).distinct().order_by('-created_at')
    
    return render(request, 'HowTo/business_guides.html', {
        'business': business,
        'how_tos': how_tos
    })
