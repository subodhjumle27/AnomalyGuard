import pandas as pd
import sqlite3
import json
import re
from datetime import datetime

class FormatValidator:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def detect(self, df=None):
        """
        Validates the format of transaction data.
        """
        if df is None:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
            conn.close()

        # Normalize columns for CSV input
        if 'vendor' in df.columns:
            df = df.rename(columns={'vendor': 'vendor_name', 'date': 'transaction_date', 'type': 'transaction_type'})

        findings = []
        for _, row in df.iterrows():
            errors = []
            
            # 1. Amount validation
            amount = row.get('amount')
            try:
                if amount is not None:
                    float_amount = float(amount)
                    if float_amount <= 0:
                        errors.append(f"Invalid amount: {amount} (must be positive)")
            except (ValueError, TypeError):
                errors.append(f"Invalid amount format: {amount}")

            # 2. Date validation
            date_str = row.get('transaction_date')
            if date_str:
                try:
                    dt = pd.to_datetime(date_str)
                    if dt > datetime.now():
                        errors.append(f"Future transaction date: {date_str}")
                    if dt.year < 2000:
                        errors.append(f"Suspiciously old transaction date: {date_str}")
                except Exception:
                    errors.append(f"Invalid date format: {date_str}")

            if errors:
                findings.append({
                    'transaction_id': row['transaction_id'],
                    'detector_type': 'statistical',
                    'detector_name': 'FormatValidator',
                    'confidence': 1.0,
                    'severity': 'error',
                    'finding_summary': f"Format validation failed: {'; '.join(errors)}",
                    'finding_details': {
                        'format_errors': errors
                    }
                })
            
        return findings

    def save_findings(self, findings):
        """Saves findings to the anomaly_detections table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for finding in findings:
            cursor.execute("""
                INSERT INTO anomaly_detections 
                (transaction_id, detector_type, detector_name, confidence, severity, finding_summary, finding_details_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                finding['transaction_id'],
                finding['detector_type'],
                finding['detector_name'],
                finding['confidence'],
                finding['severity'],
                finding['finding_summary'],
                json.dumps(finding['finding_details'])
            ))
            
            cursor.execute("""
                UPDATE monitored_transactions 
                SET status = 'flagged', risk_level = 'medium'
                WHERE transaction_id = ? AND risk_level IN ('low', 'info')
            """, (finding['transaction_id'],))
            
        conn.commit()
        conn.close()
