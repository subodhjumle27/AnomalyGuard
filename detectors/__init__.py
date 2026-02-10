from .duplicate_detector import DuplicateDetector
from .outlier_detector import OutlierDetector
from .missing_field_detector import MissingFieldDetector
from .format_validator import FormatValidator
from .temporal_anomaly_detector import TemporalAnomalyDetector
from rules.business_rules import BusinessRuleEngine
from analyzers.llm_analyzer import LLMAnalyzer
from analyzers.risk_scorer import RiskScorer
import pandas as pd
import sqlite3
import json

class DetectionPipeline:
    def __init__(self, db_path='anomalyguard.db'):
        self.db_path = db_path
        self.detectors = [
            DuplicateDetector(db_path),
            OutlierDetector(db_path),
            MissingFieldDetector(db_path),
            FormatValidator(db_path),
            TemporalAnomalyDetector(db_path),
            BusinessRuleEngine(db_path)
        ]
        self.llm_analyzer = LLMAnalyzer()
        self.risk_scorer = RiskScorer(db_path)

    def run_all(self, df=None):
        """Runs all registered detectors on the data."""
        total_findings = []
        for detector in self.detectors:
            findings = detector.detect(df)
            detector.save_findings(findings)
            total_findings.extend(findings)
        return total_findings

    def enrich_with_ai(self):
        """Processes flagged transactions with LLM for deeper insight."""
        conn = sqlite3.connect(self.db_path)
        # Get detections that haven't been analyzed by LLM yet
        query = "SELECT id, transaction_id, finding_summary FROM anomaly_detections WHERE llm_context_analysis IS NULL"
        detections = pd.read_sql_query(query, conn)
        
        enriched_count = 0
        for _, det in detections.iterrows():
            # Get transaction data
            cursor = conn.cursor()
            cursor.execute("SELECT data_json FROM monitored_transactions WHERE transaction_id = ?", (det['transaction_id'],))
            row = cursor.fetchone()
            if not row: continue
            
            txn_data = json.loads(row[0])
            llm_results = self.llm_analyzer.analyze_anomaly(txn_data, det['finding_summary'])
            
            self.risk_scorer.update_anomaly_risk(det['id'], llm_results)
            enriched_count += 1
            
        conn.close()
        return enriched_count
