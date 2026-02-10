# AnomalyGuard - Automated Data Quality & Anomaly Detection System
## 🧠 Brain.md - Technical Specification & Progress Tracker

---

## 📊 PROJECT STATUS

**Current Phase:** ✅ DONE (Ready for Deploy)  
**Last Updated:** 2026-02-10 19:40 IST  
**Progress:** 100% Complete  
**Next Session Goal:** Final Deployment & Recording
  

### Session Progress Log
```
Session 1 (2026-02-10): 
  ✅ Project setup
  ✅ Data ingestion module
  ✅ Statistical checks

Session 2 (2026-02-10):
  ✅ Core detection suite
  ✅ Business rule engine
  ✅ Detection pipeline

Session 3 (2026-02-10):
  ✅ LLM integration (Groq)
  ✅ Risk scoring algorithm
  ✅ Contextual AI enrichment

Session 4 (2026-02-10):
  ✅ Dashboard UI with Plotly charts
  ✅ Review interface with audit trail
  ✅ Transaction status management

Session 5 (2026-02-10):
  ✅ Demo script & sample data
  ✅ Polish & final verification
  ✅ Project documentation complete
```

---

## 🎯 PROJECT SCOPE & POSITIONING

### Standalone vs Integrated?
**Decision: STANDALONE PROJECT (Separate Repo)**

**Why Separate:**
- ✅ Shows portfolio breadth (2 different systems)
- ✅ AnomalyGuard monitors ANY data source (not just DocuFlow)
- ✅ Different core functionality (monitoring vs processing)
- ✅ Can be sold/demoed independently
- ✅ Better for GitHub portfolio (2 repos > 1 monolith)

**Optional Integration:**
- Can connect to DocuFlow's database as one data source
- Design with generic data ingestion (CSV, API, SQL)
- Demo can show them working together, but not required

**Folder Structure Decision:**
```
portfolio/
├── docuflow-ai/           # Project 1 (DONE ✅)
│   ├── app.py
│   ├── database/
│   └── README.md
│
└── anomalyguard/          # Project 2 (THIS PROJECT)
    ├── app.py
    ├── detectors/
    ├── analyzers/
    └── README.md
```

---

## 🎬 PROJECT OVERVIEW

### Elevator Pitch
"AnomalyGuard is an AI-powered data quality monitoring system that continuously scans accounting data for anomalies, validates business rules, and uses LLMs to assess risk context. It catches errors before they become audit problems."

### Business Value
- **Problem:** Accounting firms process thousands of transactions monthly, errors slip through manual review
- **Solution:** Automated 24/7 monitoring with hybrid statistical + AI detection
- **Impact:** Reduce data errors by 85%, catch issues in minutes vs days, full audit trail

### Target User
- Accounting firms (Countable.co's customers)
- Finance teams in companies
- Auditors needing data validation
- Anyone managing financial data at scale

---

## 🛠️ TECHNICAL STACK

### Core Technologies
**Framework:** Streamlit (consistent with DocuFlow)  
**Language:** Python 3.11+  
**Database:** SQLite (can upgrade to PostgreSQL)  
**AI/LLM:** OpenAI API (GPT-4.1 Nano, specifically gpt-4.1-nano-2025-04-14)  
**Data Processing:** Pandas, NumPy, SciPy  
**Visualization:** Plotly (for charts), Streamlit native charts  

### Key Libraries
```python
# requirements.txt
streamlit==1.31.0
pandas==2.2.0
numpy==1.26.0
scipy==1.12.0
openai==1.12.0
sqlalchemy==2.0.25
plotly==5.18.0
python-dateutil==2.8.2
python-dotenv==1.0.0
```

### Deployment
- **Hosting:** Streamlit Community Cloud (FREE)
- **Cost:** $0/month (Groq free tier)
- **Deployment Time:** 5 minutes

---

## 📐 DATABASE SCHEMA

```sql
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
```

---

## 🔬 DETECTION MODULES

### 1. Duplicate Detector
- Exact matching on key fields (date, amount, vendor)
- Fuzzy matching for vendor names
- Time window filtering (24 hours)
- Confidence: 95% for exact, 60-80% for fuzzy

### 2. Outlier Detector
- Z-score method (>3 std deviations)
- IQR method (1.5x interquartile range)
- Per-vendor outlier detection
- Confidence: 70-90%

### 3. Missing Field Detector
- Required field validation
- Empty value detection
- Format checks
- Confidence: 100% (deterministic)

### 4. Format Validator
- Date validation (not future, reasonable range)
- Amount validation (positive, proper format)
- Pattern matching (invoice numbers, etc.)
- Confidence: 100% (deterministic)

### 5. Temporal Anomaly Detector
- Weekend entry detection
- Holiday entry detection
- Unusual time detection
- Volume spike detection
- Confidence: 60-80% (context-dependent)

### 6. AI Risk Analyzer
- LLM contextual analysis using Groq
- Risk assessment (low/medium/high/critical)
- Explanation generation
- Combined scoring with statistical signals

---

## 📁 PROJECT STRUCTURE

```
anomalyguard/
├── app.py                              # Main Streamlit app
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── brain.md                            # THIS FILE
│
├── database/
│   ├── schema.sql
│   ├── init_db.py
│   └── seed_data.py
│
├── detectors/
│   ├── __init__.py
│   ├── duplicate_detector.py
│   ├── outlier_detector.py
│   ├── missing_field_detector.py
│   ├── format_validator.py
│   └── temporal_anomaly_detector.py
│
├── analyzers/
│   ├── __init__.py
│   ├── llm_analyzer.py
│   ├── risk_scorer.py
│   └── pattern_analyzer.py
│
├── rules/
│   ├── __init__.py
│   ├── business_rules.py
│   ├── threshold_rules.py
│   └── custom_rules.py
│
├── ui/
│   ├── __init__.py
│   ├── ingestion_page.py
│   ├── dashboard_page.py
│   ├── review_page.py
│   ├── analytics_page.py
│   └── config_page.py
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── export_utils.py
│   └── audit_logger.py
│
├── samples/
│   ├── sample_transactions.csv
│   ├── sample_with_anomalies.csv
│   └── integration_with_docuflow.csv
│
└── docs/
    ├── architecture.png
    ├── demo_script.md
    └── api_integration.md
```

---

## 🚀 DEVELOPMENT PHASES

### Phase 1: Foundation (2-3 hours)
**Goal:** Data ingestion + database + basic detection

- [ ] Set up project structure
- [ ] Create SQLite database with schema
- [ ] Build data ingestion module (CSV upload)
- [ ] Implement duplicate detector
- [ ] Implement outlier detector (Z-score method)
- [ ] Basic Streamlit UI for upload + results display

**Checkpoint:** Can upload CSV and see duplicate/outlier detections

---

### Phase 2: Core Detection Engine (2 hours)
**Goal:** Complete statistical detection suite

- [ ] Implement missing field detector
- [ ] Implement format validator
- [ ] Implement temporal anomaly detector
- [ ] Build business rule engine (threshold rules)
- [ ] Create combined detection pipeline
- [ ] Add severity scoring

**Checkpoint:** All 5 detector types working with confidence scores

---

### Phase 3: AI Analysis Layer (1.5 hours)
**Goal:** LLM integration + risk scoring

- [ ] Set up OpenAI API integration
- [ ] Build LLM prompt for contextual analysis
- [ ] Implement JSON parsing from LLM response
- [ ] Create combined risk scoring algorithm
- [ ] Add risk level categorization
- [ ] Store analysis results in database

**Checkpoint:** Flagged transactions get AI risk assessment

---

### Phase 4: User Interface (2 hours)
**Goal:** Complete Streamlit UI with all pages

- [ ] Build dashboard page (metrics + priority queue)
- [ ] Build review interface (side-by-side view)
- [ ] Add edit/approve/reject functionality
- [ ] Build analytics page (charts + trends)
- [ ] Build rule configuration page
- [ ] Polish UI with Streamlit components

**Checkpoint:** Full UI navigation working

---

### Phase 5: Polish & Deploy (1 hour)
**Goal:** Production-ready deployment

- [ ] Add sample data files
- [ ] Write comprehensive README
- [ ] Create demo script for interview
- [ ] Add error handling and loading states
- [ ] Test with edge cases
- [ ] Deploy to Streamlit Cloud
- [ ] Record demo video

**Checkpoint:** Live demo URL + GitHub repo ready

---

**Total Estimated Time: 8-9 hours**

---

## 🔗 INTEGRATION WITH DOCUFLOW (Optional)

### Can They Work Together?

**Yes - but as separate systems that share data**

**Integration Option 1: Database Connection**
```python
# AnomalyGuard can read from DocuFlow's database
def load_from_docuflow():
    docuflow_db = sqlite3.connect('../docuflow-ai/documents.db')
    query = "SELECT * FROM extracted_data WHERE status='approved'"
    return pd.read_sql(query, docuflow_db)
```

**Integration Option 2: CSV Export/Import**
- DocuFlow exports processed invoices to CSV
- AnomalyGuard imports and analyzes
- Simplest for demo purposes

**Demo Narrative:**
"DocuFlow handles document processing and extraction. AnomalyGuard provides a second layer of quality control by analyzing the extracted data for anomalies. Together they create a two-layer validation system."

---

## 🎯 JOB REQUIREMENT MAPPING

### How This Project Demonstrates Required Skills

✅ **LLMs and applied AI** - Groq LLM for contextual risk analysis  
✅ **Automation platforms** - Automated 24/7 monitoring system  
✅ **APIs, webhooks** - Can ingest via API, integrates with other systems  
✅ **Structured data handling** - SQLite database, pandas processing  
✅ **Process mapping** - Detection pipeline architecture  
✅ **Risk assessment** - Multi-layer risk scoring  
✅ **Quality control** - Validates data quality, catches errors  
✅ **ROI modeling** - Metrics show time saved, errors prevented  
✅ **Governance & Reliability** - Audit trails, threshold enforcement  
✅ **Continuous Optimization** - False positive tracking, rule tuning  

---

## 📝 DEMO SCRIPT FOR INTERVIEW

### Opening (30 seconds)
"This is AnomalyGuard - it continuously monitors accounting data for errors and fraud patterns. What used to require periodic manual audits now happens in real-time with 24/7 automated detection."

### Demo Flow (2.5 minutes)

**1. Ingestion (20 sec)**
- Upload sample CSV with 500 transactions
- "System ingests and immediately starts analyzing"

**2. Dashboard (30 sec)**
- Show metrics: 500 processed, 27 anomalies detected
- Show risk distribution
- "Priority queue shows 5 items needing human review"

**3. Detection Examples (60 sec)**
- Click CRITICAL item: duplicate transaction
- Show statistical detection + AI analysis
- Show outlier detection example

**4. Review Workflow (30 sec)**
- Edit a field
- Approve with notes
- Show audit trail

**5. Analytics (20 sec)**
- Show detection accuracy metrics
- Show trend chart

### Business Value (20 sec)
"For 10,000 transactions/month, this catches 200-300 errors before auditors see them. Saves 15-20 hours of manual review monthly. Full audit trail means compliance-ready from day one."

---

## 🎓 KEY TALKING POINTS

### Technical Decisions
- **Why hybrid approach?** Statistical methods catch obvious errors, AI adds contextual reasoning
- **Why confidence scoring?** Prevents alert fatigue, tunes automation level
- **Why separate from DocuFlow?** Different concerns - extraction vs validation

### Business Thinking
- **Integration:** Non-disruptive, passive monitor
- **Success metrics:** Error catch rate, false positive rate, time saved
- **Scalability:** Designed to handle 10K+ transactions/day

---

## ✅ PROJECT CHECKLIST

### Pre-Development
- [x] Define project scope
- [x] Design system architecture
- [x] Plan database schema
- [x] Map to job requirements
- [ ] Set up development environment

### Development
- [ ] Phase 1: Foundation (2-3 hrs)
- [ ] Phase 2: Core Detection (2 hrs)
- [ ] Phase 3: AI Analysis (1.5 hrs)
- [ ] Phase 4: User Interface (2 hrs)
- [ ] Phase 5: Polish & Deploy (1 hr)

### Testing
- [ ] Create test data sets
- [ ] Test all detectors
- [ ] Test combined pipeline
- [ ] Test UI workflows

### Documentation
- [ ] README.md
- [ ] Demo script
- [ ] Architecture diagram
- [ ] Code comments

### Deployment
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Test live demo
- [ ] Record demo video

---

## 🔖 QUICK REFERENCE

**LLM API:** OpenAI (gpt-4.1-nano-2025-04-14)  
**Database:** SQLite, anomalyguard.db  
**Deployment:** Streamlit Cloud (free), 5 minutes  
**Build Time:** 8-9 hours (1 day)  
**Cost:** $0/month  

---

**END OF BRAIN.MD**

*Last updated: 2026-02-10 18:39 IST*  
*Version: 1.0*  
*Status: Ready to build*
