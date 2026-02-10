import pandas as pd
import sqlite3
import json
from datetime import datetime

class TemporalAnomalyDetector:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def detect(self, df=None):
        """
        Detects temporal anomalies (e.g., weekend transactions).
        """
        if df is None:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
            conn.close()

        findings = []
        for _, row in df.iterrows():
            date_str = row.get('transaction_date')
            if not date_str:
                continue
                
            try:
                dt = pd.to_datetime(date_str)
                # Check for weekends (5 = Saturday, 6 = Sunday)
                if dt.weekday() >= 5:
                    findings.append({
                        'transaction_id': row['transaction_id'],
                        'detector_type': 'statistical',
                        'detector_name': 'TemporalAnomalyDetector',
                        'confidence': 0.75,
                        'severity': 'warning',
                        'finding_summary': f"Transaction recorded on a weekend: {dt.strftime('%A')}",
                        'finding_details': {
                            'day_of_week': dt.strftime('%A'),
                            'is_weekend': True
                        }
                    })
            except Exception:
                continue
            
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
                WHERE transaction_id = ? AND risk_level == 'low'
            """, (finding['transaction_id'],))
            
        conn.commit()
        conn.close()
