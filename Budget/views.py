from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.template.loader import render_to_string
from Product.models import Product
from Photo.models import ProductPhoto
from .models import Budget, BudgetCategory, BudgetItem
from .forms import BudgetForm, CategoryForm

@login_required
def BudgetListView(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'Budget/budget_list.html', {'budgets': budgets})

@login_required
def BudgetDetailView(request, budg_id):
    budget = get_object_or_404(Budget, id=budg_id, user=request.user)
    return render(request, "Budget/budget_detail.html", {"budget": budget})

# HTMX Views
@login_required
def hx_create_budget_modal(request):
    form = BudgetForm()
    return render(request, 'Budget/partials/create_budget_modal.html', {'form': form})

@login_required
@require_http_methods(['POST'])
def hx_save_budget(request):
    form = BudgetForm(request.POST)
    if form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        budget.save()
        
        category_names = request.POST.getlist('category_name[]')
        category_amounts = request.POST.getlist('category_amount[]')
        
        for name, amount in zip(category_names, category_amounts):
            if name.strip():
                BudgetCategory.objects.create(
                    budget=budget,
                    name=name,
                    allocated_amount=float(amount) if amount else 0.0
                )
        
        if request.headers.get('HX-Request'):
            return HttpResponse(status=204, headers={'HX-Trigger': 'budgetListChanged'})
        return redirect('Budget:list')
    
    return render(request, 'Budget/partials/create_budget_modal.html', {'form': form})

@login_required
def hx_budget_tab(request, budg_id, tab_name):
    budget = get_object_or_404(Budget, id=budg_id, user=request.user)
    context = {'budget': budget}
    
    if tab_name == 'overview':
        template = 'Budget/tabs/overview.html'
        categories = budget.categories.all()
        context['category_labels'] = [c.name for c in categories]
        context['category_data'] = [float(c.allocated_amount) for c in categories]
        context['any_data'] = any(context['category_data'])
        context['total_items_count'] = budget.items.count()
        context['completed_items_count'] = budget.items.filter(is_completed=True).count()
    elif tab_name == 'categories':
        template = 'Budget/tabs/categories.html'
        context['categories'] = budget.categories.all()
        context['category_form'] = CategoryForm()
    elif tab_name == 'shopping_list':
        template = 'Budget/tabs/shopping_list.html'
        context['items'] = budget.items.all().order_by('is_completed', '-added_at')
        context['categories'] = budget.categories.all()
        context['total_cost'] = budget.total_estimated_spend
    elif tab_name == 'expenses':
        template = 'Budget/tabs/expenses.html'
        context['completed_items'] = budget.items.filter(is_completed=True)
        context['total_spent'] = budget.total_actual_spend
    elif tab_name == 'forecast':
        template = 'Budget/tabs/forecast.html'
    else:
        return HttpResponse('Invalid Tab', status=400)
    
    return render(request, template, context)

@login_required
def hx_add_category_row(request):
    return render(request, 'Budget/partials/category_row.html')

@login_required
@require_http_methods(['POST'])
def hx_save_category(request, budg_id):
    budget = get_object_or_404(Budget, id=budg_id, user=request.user)
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save(commit=False)
        category.budget = budget
        category.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'categoriesChanged'})
    return render(request, 'Budget/partials/category_form.html', {'category_form': form, 'budget': budget})

@login_required
@require_http_methods(['DELETE'])
def hx_delete_category(request, cat_id):
    category = get_object_or_404(BudgetCategory, id=cat_id, budget__user=request.user)
    category.delete()
    return HttpResponse(status=204, headers={'HX-Trigger': 'categoriesChanged'})

@login_required
@require_http_methods(['POST'])
def hx_add_item_to_shopping_list(request, budg_id):
    budget = get_object_or_404(Budget, id=budg_id, user=request.user)
    product_id = request.POST.get('product_id')
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        item = BudgetItem.objects.create(
            budget=budget,
            product=product,
            name=product.name,
            selected_price=product.price
        )
    else:
        name = request.POST.get('name', 'New Item')
        item = BudgetItem.objects.create(
            budget=budget,
            name=name,
            selected_price=0.0
        )
        
    return HttpResponse(status=204, headers={'HX-Trigger': 'shoppingListChanged'})

@login_required
@require_http_methods(['POST'])
def hx_update_item(request, item_id):
    item = get_object_or_404(BudgetItem, id=item_id, budget__user=request.user)
    qty = request.POST.get('quantity')
    price = request.POST.get('price')
    category_id = request.POST.get('category_id')
    is_completed = request.POST.get('is_completed')
    
    if qty is not None:
        item.quantity = float(qty)
    if price is not None:
        item.selected_price = float(price)
    if category_id is not None:
        if category_id == "":
            item.category = None
        else:
            item.category = get_object_or_404(BudgetCategory, id=category_id, budget=item.budget)
    
    if is_completed is not None:
        item.is_completed = is_completed == 'true'
        if item.is_completed and item.actual_price is None:
            item.actual_price = item.selected_price
    item.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'shoppingListChanged'})

@login_required
@require_http_methods(['DELETE'])
def hx_delete_item(request, item_id):
    item = get_object_or_404(BudgetItem, id=item_id, budget__user=request.user)
    item.delete()
    return HttpResponse(status=204, headers={'HX-Trigger': 'shoppingListChanged'})

@login_required
def product_search(request):
    query = request.GET.get('q', '').strip()
    budget_id = request.GET.get('budget_id')
    
    if not query or len(query) < 2:
        return HttpResponse('')
    
    # Use the same logic as navbar search
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) |
        Q(business__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).select_related('business').distinct()[:10]
    
    return render(request, 'Budget/partials/product_search_results.html', {
        'products': products,
        'budget_id': budget_id,
        'query': query
    })

@login_required
@require_http_methods(['POST'])
def hx_refresh_prices(request, budg_id):
    budget = get_object_or_404(Budget, id=budg_id, user=request.user)
    items = budget.items.filter(product__isnull=False, is_completed=False)
    for item in items:
        if item.product.price != item.selected_price:
            item.selected_price = item.product.price
            item.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'shoppingListChanged'})