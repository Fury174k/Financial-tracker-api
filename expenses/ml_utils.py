# ml_utils.py

import pandas as pd
from django.utils.timezone import now
from datetime import timedelta
from .models import Expense
from sklearn.linear_model import LinearRegression
import numpy as np
from .models import PredictionLog


def get_expense_dataframe(user, period='monthly'):
    expenses = Expense.objects.filter(user=user)

    if not expenses.exists():
        return None

    df = pd.DataFrame(list(expenses.values('amount', 'date')))
    df['date'] = pd.to_datetime(df['date'])

    if period == 'weekly':
        df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
        grouped = df.groupby('week')['amount'].sum().reset_index()
        grouped = grouped.rename(columns={'week': 'period'})
    else:
        df['month'] = df['date'].dt.to_period('M').apply(lambda r: r.start_time)
        grouped = df.groupby('month')['amount'].sum().reset_index()
        grouped = grouped.rename(columns={'month': 'period'})

    return grouped


def predict_next(user, period='monthly'):
    df = get_expense_dataframe(user, period)

    if df is None or len(df) < 3:
        return {
            "success": False,
            "message": f"Not enough {period} data to make predictions. At least 3 data points required.",
            "prediction": None,
            "history": []
        }

    df['timestamp'] = (df['period'] - df['period'].min()).dt.days
    X = df[['timestamp']]
    y = df['amount']

    model = LinearRegression()
    model.fit(X, y)

    # Predict the next period
    last_timestamp = df['timestamp'].max()
    next_timestamp = last_timestamp + (7 if period == 'weekly' else 30)
    next_amount = model.predict([[next_timestamp]])[0]

    next_period_start = (df['period'].max() + pd.Timedelta(days=(7 if period == 'weekly' else 30))).date()

    PredictionLog.objects.create(
        user=user,
        period_type=period,
        predicted_amount=round(next_amount, 2),
        target_period_start=next_period_start
    )

    prediction_series = df[['period', 'amount']].copy()
    prediction_series = prediction_series.rename(columns={"amount": "actual"})
    prediction_series['predicted'] = None

    return {
        "success": True,
        "prediction": round(next_amount, 2),
        "history": prediction_series.to_dict(orient='records'),
        "next_period": str(next_period_start)
    }