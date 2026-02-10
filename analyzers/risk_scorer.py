import sqlite3
import json

class RiskScorer:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path

    def calculate_score(self, statistical_confidence, detector_severity, llm_modifier=0):
        """
        Calculates a combined risk score between 0 and 1.
        """
        severity_map = {
            'info': 0.1,
            'warning': 0.4,
            'error': 0.8,
            'critical': 1.0
        }
        
        base_score = severity_map.get(detector_severity, 0.5) * statistical_confidence
        combined_score = base_score + llm_modifier
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, combined_score))

    def get_risk_level(self, score):
        if score >= 0.9: return 'critical'
        if score >= 0.7: return 'high'
        if score >= 0.4: return 'medium'
        return 'low'

    def update_anomaly_risk(self, detection_id, llm_results):
        """Updates an anomaly detection with LLM results and a combined score."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get original detection data
        cursor.execute("SELECT confidence, severity, transaction_id FROM anomaly_detections WHERE id = ?", (detection_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return
            
        confidence, severity, transaction_id = row
        
        # Calculate new score
        llm_modifier = llm_results.get('risk_score_modifier', 0)
        combined_score = self.calculate_score(confidence, severity, llm_modifier)
        risk_level = self.get_risk_level(combined_score)
        
        # Update detection record
        cursor.execute("""
            UPDATE anomaly_detections
            SET llm_context_analysis = ?,
                llm_risk_assessment = ?,
                combined_risk_score = ?,
                suggested_action = ?
            WHERE id = ?
        """, (
            llm_results.get('context_analysis'),
            llm_results.get('risk_assessment'),
            combined_score,
            llm_results.get('suggested_action'),
            detection_id
        ))
        
        # Update transaction risk level
        cursor.execute("""
            UPDATE monitored_transactions
            SET risk_level = ?
            WHERE transaction_id = ?
        """, (risk_level, transaction_id))
        
        conn.commit()
        conn.close()
        return combined_score
