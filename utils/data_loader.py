import pandas as pd
import sqlite3
import json
import uuid
from datetime import datetime

class DataLoader:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def load_csv(self, file_path):
        """Loads a CSV file into a pandas DataFrame."""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

    def ingest_dataframe(self, df, source_name='csv_upload'):
        """Ingests a DataFrame into the monitored_transactions table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        ingested_count = 0
        for _, row in df.iterrows():
            transaction_id = str(row.get('transaction_id', uuid.uuid4()))
            data_json = row.to_json()
            transaction_date = row.get('date') or row.get('transaction_date')
            amount = row.get('amount')
            vendor_name = row.get('vendor') or row.get('vendor_name')
            transaction_type = row.get('type') or row.get('transaction_type')
            
            try:
                cursor.execute("""
                    INSERT INTO monitored_transactions 
                    (transaction_id, source, data_json, transaction_date, amount, vendor_name, transaction_type, status, risk_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    transaction_id, 
                    source_name, 
                    data_json, 
                    transaction_date, 
                    amount, 
                    vendor_name, 
                    transaction_type, 
                    'clean', 
                    'low'
                ))
                ingested_count += 1
            except sqlite3.IntegrityError:
                # Skip duplicates based on transaction_id
                continue
                
        conn.commit()
        conn.close()
        return ingested_count

    def get_all_transactions(self):
        """Retrieves all transactions from the database."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
        conn.close()
        return df
