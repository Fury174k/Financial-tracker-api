from rest_framework import generics, permissions
from .models import Expense, Account, Transaction, Budget, SavingsGoal, SavingsContribution, PredictionLog, Notification
from .serializers import ExpenseSerializer, AccountSerializer, TransactionSerializer, BudgetSerializer, SavingsGoalSerializer, SavingsContributionSerializer, PredictionLogSerializer, NotificationSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=201)

    

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expense = serializer.save(user=self.request.user)
        expense.account.balance -= expense.amount
        expense.account.save()

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class TotalBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        total_balance = sum(account.balance for account in accounts)
        return Response({'total_balance': total_balance})


class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        if transaction.type == 'expense':
            transaction.account.balance -= transaction.amount
        elif transaction.type == 'income':
            transaction.account.balance += transaction.amount
        transaction.account.save()

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class GoogleAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(token, Request(), settings.GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = idinfo['email']
            name = idinfo.get('name', '')
            
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0],
                'first_name': name
            })

            # Check if user has bank accounts
            has_bank_account = user.accounts.exists()  # Use correct related_name from Account model

            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True, 
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'profile_picture': user.profile_picture.url if user.profile_picture else idinfo.get('picture', None)
                },
                'has_bank_account': has_bank_account
            }, status=200)
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=400)

class CurrentBudgetView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        month = now.month
        year = now.year
        budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
        if budget:
            return Response({'amount': budget.amount})
        return Response({'amount': None}, status=404)

    def post(self, request):
        now = timezone.now()
        month = now.month
        year = now.year
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        budget, created = Budget.objects.get_or_create(
            user=request.user, month=month, year=year,
            defaults={'amount': amount}
        )
        if not created:
            budget.amount = amount
            budget.save()
        return Response({'amount': budget.amount}, status=201 if created else 200)

class SavingsGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingsGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

class SavingsContributionCreateView(generics.CreateAPIView):
    serializer_class = SavingsContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        contribution = serializer.save(user=self.request.user)
        # Update the saved amount on the related SavingsGoal
        goal = contribution.goal
        goal.saved += contribution.amount
        goal.save()

class PredictionLogListView(generics.ListAPIView):
    serializer_class = PredictionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PredictionLog.objects.filter(user=self.request.user)        

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_active=True).order_by('-created_at')

class NotificationDeleteView(generics.DestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)  

class MarkNotificationReadView(APIView):
    def post(self, request, pk):
        try:
            notif = Notification.objects.get(id=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return Response({'message': 'Marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)