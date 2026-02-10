-- Main transaction monitoring table
CREATE TABLE monitored_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT UNIQUE NOT NULL,
    source TEXT,
    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_json TEXT NOT NULL,
    transaction_date DATE,
    amount REAL,
    vendor_name TEXT,
    transaction_type TEXT,
    status TEXT CHECK(status IN ('clean', 'flagged', 'reviewed', 'escalated')),
    risk_level TEXT CHECK(risk_level IN ('low', 'medium', 'high', 'critical'))
);

-- Anomaly detections
CREATE TABLE anomaly_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT REFERENCES monitored_transactions(transaction_id),
    detection_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    detector_type TEXT,
    detector_name TEXT,
    confidence REAL,
    severity TEXT CHECK(severity IN ('info', 'warning', 'error', 'critical')),
    finding_summary TEXT,
    finding_details_json TEXT,
    suggested_action TEXT,
    llm_context_analysis TEXT,
    llm_risk_assessment TEXT,
    combined_risk_score REAL
);

-- Business rules configuration
CREATE TABLE business_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT UNIQUE NOT NULL,
    rule_type TEXT,
    rule_definition_json TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Review actions (audit trail)
CREATE TABLE review_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT REFERENCES monitored_transactions(transaction_id),
    detection_id INTEGER REFERENCES anomaly_detections(id),
    action_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    action_type TEXT,
    reviewer TEXT DEFAULT 'system',
    notes TEXT,
    resolution TEXT,
    corrected_data_json TEXT
);
