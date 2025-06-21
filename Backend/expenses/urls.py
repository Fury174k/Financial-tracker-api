from django.urls import path
from .views import (
    ExpenseListCreateView,
    ExpenseDetailView,
    TotalBalanceView,
    AccountListCreateView,
    RegisterView,
    UserDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    GoogleAuthView,
    CurrentBudgetView,
    SavingsGoalListCreateView,
    SavingsGoalDetailView,
    SavingsContributionCreateView,
    PredictionLogListView,
    NotificationDeleteView,
    NotificationListView,
    MarkNotificationReadView                # <-- add this import
)
from rest_framework.authtoken.views import obtain_auth_token
from .analytics import WeeklySpendingView, TopExpensesView, CategorySpendingView, PredictionView, WeeklyPredictionView, MonthlyPredictionView

urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('total-balance/', TotalBalanceView.as_view(), name='total-balance'),
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'), 
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('auth/google/', GoogleAuthView.as_view(), name='google-auth'),
    path('budget/current/', CurrentBudgetView.as_view(), name='current-budget'),
    path('savings/', SavingsGoalListCreateView.as_view(), name='savings-list-create'),
    path('savings/<int:pk>/', SavingsGoalDetailView.as_view(), name='savings-detail'),
    path('savings/contribute/', SavingsContributionCreateView.as_view(), name='savings-contribute'),
    path('analytics/weekly-spending/', WeeklySpendingView.as_view(), name='analytics-weekly'),
    path('analytics/top-expenses/', TopExpensesView.as_view(), name='analytics-top'),
    path('analytics/by-category/', CategorySpendingView.as_view(), name='analytics-category'),
    path('analytics/prediction/', PredictionView.as_view(), name='analytics-prediction'),
    path('analytics/predict-weekly/', WeeklyPredictionView.as_view(), name='predict-weekly'),
    path('analytics/predict-monthly/', MonthlyPredictionView.as_view(), name='predict-monthly'),
    path('analytics/predictions/history/', PredictionLogListView.as_view(), name='prediction-history'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/', NotificationDeleteView.as_view(), name='notification-delete'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]

