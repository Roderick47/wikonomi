from django.shortcuts import render,redirect
from django.contrib import messages

from .models import Budget
from .forms import BudgetAddForm

# Create your views here.


def BudgetListView(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request,'Budget/budget_list.html',{'budgets':budgets})

def BudgetDetailView(request,budg_id):
    budget = Budget.object.get(id=budg_id)
    return render(request,"BUdget/budget_detail.html",{"budget":budget})

def CreateBudgetView(request):
    #Check to see if the user is authenticated. then returns back to their previous page.
    if request.user.is_authenticated:
        if request.method =="POST":
            form=BudgetAddForm(request.POST)
            if form.is_valid():
                budget=form.save(commit=False)
                budget.user = request.user
                budget.save()
                return redirect('Budget:detail',budg_id=budget.id)
    form=BudgetAddForm()
    return render(request,'Budget/budget_add_form.html',{'form':form})
    
        
        