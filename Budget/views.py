from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from Product.models import Product
from .models import Budget
from .forms import BudgetAddForm

# Create your views here.


def BudgetListView(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request,'Budget/budget_list.html',{'budgets':budgets})

def BudgetDetailView(request,budg_id):
    budget = Budget.objects.get(id=budg_id)
    return render(request,"Budget/budget_detail.html",{"budget":budget})

def CreateBudgetView(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == "POST":
        form = BudgetAddForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            # Save the many-to-many relationship
            form.save_m2m()
            messages.success(request, 'Budget created successfully!')
            return redirect('Budget:detail', budg_id=budget.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BudgetAddForm()
        
    return render(request, 'Budget/budget_add_form.html', {'form': form})


@csrf_exempt
@require_http_methods(['POST'])
@login_required(login_url='/accounts/login/')
def api_add_to_budget(request, budget_id, product_id):
    """API endpoint to add a product to a budget"""
    try:
        budget = get_object_or_404(Budget, id=budget_id, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is already in the budget
        if budget.products.filter(id=product_id).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Product already exists in this budget'
            }, status=400)
            
        # Add product to budget
        budget.products.add(product)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product added to budget successfully',
            'budget': {
                'id': budget.id,
                'title': budget.title,
                'product_count': budget.products.count()
            },
            'product': {
                'id': product.id,
                'name': product.name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(['GET'])
@login_required(login_url='/accounts/login/')
def api_list_budgets(request):
    """API endpoint to list all budgets for the current user"""
    try:
        budgets = Budget.objects.filter(user=request.user).values('id', 'title')
        
        # Add product count to each budget
        budgets_list = []
        for budget in budgets:
            budget_data = dict(budget)
            budget_data['product_count'] = Budget.objects.get(id=budget['id']).products.count()
            budgets_list.append(budget_data)
            
        return JsonResponse({
            'status': 'success',
            'budgets': list(budgets_list)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)