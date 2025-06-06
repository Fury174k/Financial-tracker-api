from .views import ExpenseListCreateView
from django.urls import path


urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
]