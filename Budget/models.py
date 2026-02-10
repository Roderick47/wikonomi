from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from django.utils import timezone

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('CUSTOM', 'Custom'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='MONTHLY')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Existing legacy field - keeping for now
    products = models.ManyToManyField(Product, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']

    @property
    def total_allocated(self):
        return sum(cat.allocated_amount for cat in self.categories.all())

    @property
    def total_estimated_spend(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_actual_spend(self):
        return sum(item.total_price for item in self.items.filter(is_completed=True))

    @property
    def progress_percentage(self):
        estimated = self.total_estimated_spend
        if self.target_amount > 0:
            return min(int((estimated / self.target_amount) * 100), 100)
        return 0

class BudgetCategory(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} - {self.budget.title}"

    @property
    def actual_spend(self):
        return sum(item.total_price for item in self.items.filter(is_completed=True))

    @property
    def estimated_spend(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def progress_percentage(self):
        if self.allocated_amount > 0:
            return min(int((self.estimated_spend / self.allocated_amount) * 100), 100)
        return 0

class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    selected_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    actual_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} x {self.quantity}"

    @property
    def current_price(self):
        if self.is_completed and self.actual_price is not None:
            return self.actual_price
        return self.selected_price

    @property
    def total_price(self):
        return self.current_price * self.quantity