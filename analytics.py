"""
analytics.py - Metrics, Streaks, and Analytics Calculation
Author: College Project
Description: Provides statistical computations, streak tracking, and chart preparation.
"""

from datetime import date, timedelta
import random

MOTIVATIONAL_QUOTES = [
    "“We are what we repeatedly do. Excellence, then, is not an act, but a habit.” – Will Durant",
    "“Small daily improvements over time lead to stunning results.” – Robin Sharma",
    "“Success is the sum of small efforts, repeated day in and day out.” – Robert Collier",
    "“Discipline is choosing between what you want now and what you want most.” – Abraham Lincoln",
    "“Action is the foundational key to all success.” – Pablo Picasso"
]

def get_random_quote():
    return random.choice(MOTIVATIONAL_QUOTES)

def calculate_streaks(all_logs):
    """
    Calculate current streak and max streak across all completed routines.
    Returns: (current_streak, longest_streak)
    """
    if not all_logs:
        return 0, 0

    # Group completed days
    completed_days = set()
    # We consider a day "successful" if at least 1 routine was marked completed
    for row in all_logs:
        if row.get("completed") == 1:
            completed_days.add(row["log_date"])

    if not completed_days:
        return 0, 0

    sorted_days = sorted([date.fromisoformat(d) for d in completed_days])
    
    # Calculate current streak
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    current_streak = 0
    check_day = today if today in sorted_days else yesterday
    
    while check_day in sorted_days:
        current_streak += 1
        check_day -= timedelta(days=1)

    # Calculate max streak
    max_streak = 0
    temp_streak = 0
    last_day = None

    for d in sorted_days:
        if last_day is None or d == last_day + timedelta(days=1):
            temp_streak += 1
        else:
            temp_streak = 1
        last_day = d
        if temp_streak > max_streak:
            max_streak = temp_streak

    return current_streak, max(max_streak, current_streak)

def get_weekly_trend(all_logs, days_count=7):
    """
    Returns completion counts per day for the last N days.
    """
    today = date.today()
    date_list = [today - timedelta(days=i) for i in range(days_count - 1, -1, -1)]
    
    trend = []
    for d in date_list:
        d_str = d.isoformat()
        day_logs = [l for l in all_logs if l["log_date"] == d_str]
        completed = sum(1 for l in day_logs if l.get("completed") == 1)
        total = len(day_logs)
        rate = round((completed / total) * 100, 1) if total > 0 else 0.0
        
        trend.append({
            "Date": d.strftime("%b %d (%a)"),
            "Completed": completed,
            "Total": total,
            "Completion Rate (%)": rate
        })
    return trend

def get_category_breakdown(routines):
    """
    Calculate the count and percentage of routines per category.
    """
    if not routines:
        return {}
    breakdown = {}
    for r in routines:
        cat = r.get("category", "General")
        breakdown[cat] = breakdown.get(cat, 0) + 1
    return breakdown
