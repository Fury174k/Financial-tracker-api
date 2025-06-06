from django.shortcuts import render
from .serializers import ExpenseSerializer
from rest_framework import generics
from .models import Expense

# Create your views here.
class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer