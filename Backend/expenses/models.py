from django.db import models

# Create your models here.
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRANSPORT', 'Transport'),
        ('UTILITIES', 'Utilities'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ${self.amount}"