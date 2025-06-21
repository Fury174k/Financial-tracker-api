from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    """
    Custom user model extending Django's AbstractUser.
    Add custom fields here if needed in the future.
    """
    class Meta:
        # Not strictly needed if your app is named 'expenses'
        # Django automatically uses the app label from your app config
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username  # Or any other identifier

 

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='user'  # Adds a human-readable name in admin
    )
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='expenses') 
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='amount'
    )
    category = models.CharField(max_length=100, verbose_name='category')
    description = models.TextField(blank=True, verbose_name='description')
    date = models.DateField(default=now, verbose_name='date')
    
    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-date']  # Default ordering
    
    def __str__(self):
        return f"{self.date}: {self.category} - ${self.amount}"

class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='user'
    )
    account_number = models.CharField(
        max_length=20,
        verbose_name='account number'
    )
    bank_name = models.CharField(
        max_length=100,
        verbose_name='bank name'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='balance'
    )
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        unique_together = [['user', 'account_number']]  # Prevent duplicate accounts
    
    def __str__(self):
        return f"{self.bank_name} ({self.account_number[-4:]}) - ${self.balance}"

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='user'
    )
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='amount'
    )
    category = models.CharField(max_length=100, verbose_name='category')
    description = models.TextField(blank=True, verbose_name='description')
    date = models.DateField(default=now, verbose_name='date')
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')], verbose_name='type')
    title = models.CharField(max_length=255, blank=True, verbose_name='title')

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date']

    def __str__(self):
        return f"{self.date}: {self.type} - ${self.amount}"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.description
        super().save(*args, **kwargs)

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    month = models.PositiveSmallIntegerField()  # 1-12
    year = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year} Budget"
    
class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
    title = models.CharField(max_length=100)
    target = models.DecimalField(max_digits=12, decimal_places=2)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (${self.saved}/${self.target})"

class SavingsContribution(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='contributions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} contributed ${self.amount} to {self.goal.title} on {self.date}"
    
class PredictionLog(models.Model):
    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    predicted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    predicted_on = models.DateTimeField(auto_now_add=True)
    target_period_start = models.DateField()
    
    class Meta:
        ordering = ['-predicted_on']

    def __str__(self):
        return f"{self.user.username} - {self.period_type} prediction on {self.predicted_on.date()}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.title[:30]}"        
