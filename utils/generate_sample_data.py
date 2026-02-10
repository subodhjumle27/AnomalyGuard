import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid

def generate_data(num_rows=200):
    vendors = [
        ('Amazon', 'office_supplies', 50, 500),
        ('Staples', 'office_supplies', 20, 300),
        ('Uber', 'travel', 15, 80),
        ('Delta Airlines', 'travel', 200, 1500),
        ('Hilton Hotels', 'travel', 100, 800),
        ('WeWork', 'rent', 1000, 1500),
        ('Starbucks', 'meals', 5, 25),
        ('Chipotle', 'meals', 10, 40),
        ('AWS', 'software', 100, 2000),
        ('Slack', 'software', 50, 200),
        ('Consultant John Doe', 'services', 1000, 5000)
    ]

    data = []
    base_date = datetime.now() - timedelta(days=90)

    # 1. Generate Normal Traffic
    for _ in range(num_rows):
        vendor, v_type, min_amt, max_amt = random.choice(vendors)
        
        # Random date in last 90 days, avoiding weekends mostly
        day_offset = random.randint(0, 90)
        txn_date = base_date + timedelta(days=day_offset)
        
        # Simple adjustment to avoid weekends for normal traffic (Monday=0, Sunday=6)
        if txn_date.weekday() >= 5: 
            txn_date -= timedelta(days=2)

        amount = round(random.uniform(min_amt, max_amt), 2)
        txn_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
        
        data.append({
            'transaction_id': txn_id,
            'date': txn_date.strftime('%Y-%m-%d'),
            'amount': amount,
            'vendor': vendor,
            'type': v_type
        })

    # 2. Inject Anomalies
    
    # A. Duplicates (The "Double Click" Error)
    # Replicate 3 transactions exactly
    for i in range(3):
        original = data[i].copy()
        original['transaction_id'] = f"TXN_DUP_{i}"
        data.append(original)

    # B. Outliers (The "Fat Finger" Error)
    # Add a massive amount for a small vendor
    data.append({
        'transaction_id': 'TXN_OUTLIER_1',
        'date': (base_date + timedelta(days=45)).strftime('%Y-%m-%d'),
        'amount': 25000.00,
        'vendor': 'Uber',
        'type': 'travel'
    })
    
    # C. Weekend/Holiday Anomalies
    # Large transaction on a Sunday
    sunday = base_date + timedelta(days= (6 - base_date.weekday() + 7) % 7 )
    data.append({
        'transaction_id': 'TXN_WEEKEND_1',
        'date': sunday.strftime('%Y-%m-%d'),
        'amount': 4500.00,
        'vendor': 'Apple Store',
        'type': 'equipment'
    })

    # D. Contextual/AI Anomalies
    # 1. "Split Transaction" structuring (just under limit)
    limit = 5000
    for i in range(3):
        data.append({
            'transaction_id': f'TXN_STRUCT_{i}',
            'date': (base_date + timedelta(days=60)).strftime('%Y-%m-%d'),
            'amount': 4950.00,
            'vendor': 'Consultant John Doe',
            'type': 'services'
        })

    # 2. Suspicious Vendor
    data.append({
        'transaction_id': 'TXN_SUS_1',
        'date': (base_date + timedelta(days=70)).strftime('%Y-%m-%d'),
        'amount': 2500.00,
        'vendor': 'Luxury Spa & Resort',
        'type': 'office_supplies'  # Mismatched category for AI to catch
    })

    # E. Missing Fields
    data.append({
        'transaction_id': 'TXN_MISSING_1',
        'date': (base_date + timedelta(days=10)).strftime('%Y-%m-%d'),
        'amount': None,
        'vendor': 'Unknown Vendor',
        'type': 'misc'
    })

    # F. Format Errors
    data.append({
        'transaction_id': 'TXN_FMT_1',
        'date': '2026-13-45', # Invalid date
        'amount': -150.00, # Negative
        'vendor': 'Refund?',
        'type': 'refund'
    })

    # Shuffle
    random.shuffle(data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_data(200)
    output_path = "samples/demo_transactions_extended.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} transactions to {output_path}")
