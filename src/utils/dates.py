from datetime import datetime, timedelta
import random

def random_past_datetime(days_back=180):
    """Generate a realistic past timestamp"""
    now = datetime.now()
    delta_days = random.randint(0, days_back)
    return now - timedelta(days=delta_days)

def random_future_date(max_days=90):
    """Generate future due dates"""
    if random.random() < 0.1:  # 10% no due date
        return None
    return datetime.now().date() + timedelta(days=random.randint(1, max_days))
