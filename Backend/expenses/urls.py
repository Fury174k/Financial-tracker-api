from django.urls import path
from .views import (
    ExpenseListCreateView,
    ExpenseDetailView,
    TotalBalanceView,
    AccountListCreateView,
    RegisterView,
    UserDetailView,
    total_balance_view
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('total-balance/', TotalBalanceView.as_view(), name='total-balance'),
     path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'), 
    path('user/', UserDetailView.as_view(), name='user-detail'), 
]

