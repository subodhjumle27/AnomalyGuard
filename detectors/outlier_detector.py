import pandas as pd
import numpy as np
import sqlite3
import json
from scipy import stats

class OutlierDetector:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def detect(self, df=None):
        """
        Detects outliers in transaction amounts using Z-score method.
        """
        if df is None:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
            conn.close()

        if df.empty or len(df) < 3:
            return []

        # Calculate Z-scores for amounts
        amounts = df['amount'].astype(float)
        z_scores = np.abs(stats.zscore(amounts))
        
        # Identify outliers (Z-score > 3)
        outlier_indices = np.where(z_scores > 3)[0]
        
        findings = []
        for idx in outlier_indices:
            row = df.iloc[idx]
            findings.append({
                'transaction_id': row['transaction_id'],
                'detector_type': 'statistical',
                'detector_name': 'OutlierDetector',
                'confidence': 0.85,
                'severity': 'warning',
                'finding_summary': f"Unusually large transaction amount: ${row['amount']}",
                'finding_details': {
                    'z_score': float(z_scores[idx]),
                    'mean_amount': float(amounts.mean()),
                    'std_dev': float(amounts.std())
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
                SET status = 'flagged', risk_level = 'medium'
                WHERE transaction_id = ? AND status != 'flagged' -- Don't overwrite higher risk
            """, (finding['transaction_id'],))
            
        conn.commit()
        conn.close()
