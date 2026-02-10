import pandas as pd
import sqlite3
import json

class BusinessRuleEngine:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def detect(self, df=None):
        """
        Runs business rules on the data.
        Example: Transactions over a certain threshold for specific vendors.
        """
        if df is None:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
            conn.close()

        findings = []
        
        # Example Rule 1: High value meals
        meal_threshold = 200.0
        meal_types = ['meals', 'entertainment']
        
        mask = (df['amount'] > meal_threshold) & (df['transaction_type'].str.lower().isin(meal_types))
        high_value_meals = df[mask]
        
        for _, row in high_value_meals.iterrows():
            findings.append({
                'transaction_id': row['transaction_id'],
                'detector_type': 'business_rule',
                'detector_name': 'HighValueMealRule',
                'confidence': 1.0,
                'severity': 'warning',
                'finding_summary': f"High value meal detected: ${row['amount']}",
                'finding_details': {
                    'threshold': meal_threshold,
                    'actual': float(row['amount']),
                    'category': row['transaction_type']
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
                WHERE transaction_id = ? AND risk_level == 'low'
            """, (finding['transaction_id'],))
            
        conn.commit()
        conn.close()
