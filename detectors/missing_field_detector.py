import pandas as pd
import sqlite3
import json

class MissingFieldDetector:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path
        self.required_fields = ['transaction_date', 'amount', 'vendor_name']

    def detect(self, df=None):
        """
        Detects transactions with missing required fields.
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
            missing = []
            for field in self.required_fields:
                val = row.get(field)
                if val is None or str(val).strip().lower() in ['nan', 'none', '', 'null']:
                    missing.append(field)
            
            if missing:
                findings.append({
                    'transaction_id': row['transaction_id'],
                    'detector_type': 'statistical',
                    'detector_name': 'MissingFieldDetector',
                    'confidence': 1.0,
                    'severity': 'error',
                    'finding_summary': f"Missing required fields: {', '.join(missing)}",
                    'finding_details': {
                        'missing_fields': missing,
                        'required_fields': self.required_fields
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
                SET status = 'flagged', risk_level = 'high'
                WHERE transaction_id = ?
            """, (finding['transaction_id'],))
            
        conn.commit()
        conn.close()
