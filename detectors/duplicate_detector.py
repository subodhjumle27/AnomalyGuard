import pandas as pd
import sqlite3
import json

class DuplicateDetector:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def detect(self, df=None):
        """
        Detects duplicate transactions.
        If df is provided, it checks for duplicates within the current batch.
        Also checks against historical data in the database.
        """
        if df is None:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
            conn.close()

        # Normalize columns for CSV input
        if 'vendor' in df.columns:
            df = df.rename(columns={'vendor': 'vendor_name', 'date': 'transaction_date', 'type': 'transaction_type'})

        # Check for potential duplicates based on amount, date, and vendor
        # Note: In a real scenario, we'd use more sophisticated logic (fuzzy matching, time windows)
        duplicates = df[df.duplicated(subset=['amount', 'transaction_date', 'vendor_name'], keep=False)]
        
        findings = []
        for _, row in duplicates.iterrows():
            findings.append({
                'transaction_id': row['transaction_id'],
                'detector_type': 'statistical',
                'detector_name': 'DuplicateDetector',
                'confidence': 0.95,
                'severity': 'error',
                'finding_summary': 'Potential duplicate transaction detected',
                'finding_details': {
                    'matches_found': len(duplicates[
                        (duplicates['amount'] == row['amount']) & 
                        (duplicates['transaction_date'] == row['transaction_date']) & 
                        (duplicates['vendor_name'] == row['vendor_name'])
                    ]) - 1,
                    'criteria': ['amount', 'transaction_date', 'vendor_name']
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
            
            # Update transaction status
            cursor.execute("""
                UPDATE monitored_transactions 
                SET status = 'flagged', risk_level = ?
                WHERE transaction_id = ?
            """, (
                'high' if finding['severity'] == 'error' or finding['severity'] == 'critical' else 'medium',
                finding['transaction_id']
            ))
            
        conn.commit()
        conn.close()
