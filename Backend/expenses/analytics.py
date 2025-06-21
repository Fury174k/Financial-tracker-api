from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta
from .models import Expense

class WeeklySpendingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday

        data = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            total = Expense.objects.filter(user=request.user, date=day).aggregate(sum=Sum('amount'))['sum'] or 0
            data.append({
                "day": day.strftime('%a'),
                "amount": float(total),
                "date": str(day)
            })
        return Response(data)


class TopExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        start_of_month = today.replace(day=1)
        expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month).order_by('-amount')[:5]
        data = [{
            "name": exp.description or exp.category,
            "amount": float(exp.amount),
            "date": str(exp.date),
            "category": exp.category
        } for exp in expenses]
        return Response(data)


class CategorySpendingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        start_of_month = today.replace(day=1)

        category_totals = Expense.objects.filter(
            user=request.user,
            date__gte=start_of_month
        ).values('category').annotate(amount=Sum('amount'))

        total = sum(ct['amount'] for ct in category_totals)
        data = [{
            "category": ct['category'],
            "amount": float(ct['amount']),
            "percentage": round((ct['amount'] / total) * 100, 2) if total > 0 else 0
        } for ct in category_totals]
        return Response(data)


class PredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Pretend ML model: take last 3 weeks and average them
        today = now().date()
        past_expenses = Expense.objects.filter(user=request.user, date__lte=today).order_by('-date')[:21]

        weekly_totals = [0, 0, 0]
        for i in range(21):
            if i < len(past_expenses):
                week_index = i // 7
                weekly_totals[week_index] += past_expenses[i].amount

        avg = sum(weekly_totals) / 3 if weekly_totals else 0
        next_month_prediction = avg * 4  # crude estimate

        data = [
            {"period": "Week 1", "actual": float(weekly_totals[2]), "predicted": None},
            {"period": "Week 2", "actual": float(weekly_totals[1]), "predicted": None},
            {"period": "Week 3", "actual": float(weekly_totals[0]), "predicted": None},
            {"period": "Week 4", "actual": None, "predicted": round(avg, 2)},
            {"period": "Next Month", "actual": None, "predicted": round(next_month_prediction, 2)}
        ]
        return Response(data)

from .ml_utils import predict_next

class WeeklyPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = predict_next(request.user, period='weekly')
        return Response(result)


class MonthlyPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = predict_next(request.user, period='monthly')
        return Response(result)