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