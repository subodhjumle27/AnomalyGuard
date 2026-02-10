import streamlit as st
import pandas as pd
import os
from utils.data_loader import DataLoader
from detectors import DetectionPipeline
from ui.dashboard_page import show_dashboard
from ui.review_page import show_review
from database.init_db import init_db

# Initialize DB if needed - Critical for Cloud Deployment
if not os.path.exists('anomalyguard.db'):
    init_db()
else:
    # Ensure tables exist even if file exists
    init_db()

# Page configuration
st.set_page_config(
    page_title="AnomalyGuard | AI Data Quality",
    page_icon="🛡️",
    layout="wide"
)

# Initialize modules
loader = DataLoader()
pipeline = DetectionPipeline()

# Sidebar
st.sidebar.title("🛡️ AnomalyGuard")
selection = st.sidebar.radio("Go to", ["Upload Data", "Dashboard", "Review Alerts"])

# Header
# Header is handled within split pages now or as a common header
st.title("🛡️ AnomalyGuard")
st.markdown("""
### Automated Data Quality & Anomaly Detection
**AnomalyGuard** acts as an always-on auditor for your financial data. 
It ingests transaction logs and uses a **hybrid detection engine** (Statistical Rules + AI Context) to catch:
- 🔴 **Process Errors**: Duplicate payments, missing fields, format violations.
- 🟠 **Fraud Indicators**: Outliers, weekend activity, suspicious vendors.
- 🟡 **Compliance Risks**: Policy violations and high-risk spending.

Instead of manual sampling, get **100% coverage** of your transaction data.
""")

if selection == "Upload Data":
    st.subheader("Step 1: Ingest Data")
    
    # 1. Option to use sample data
    use_sample = st.checkbox("Use sample data (Demo Mode)")
    
    uploaded_file = None
    if use_sample:
        sample_path = "samples/demo_transactions_extended.csv"
        if os.path.exists(sample_path):
            uploaded_file = sample_path
            st.info(f"Loaded extended sample file: `{sample_path}` (200+ rows)")
        else:
            st.error("Sample file not found!")
    else:
        uploaded_file = st.file_uploader("Choose a CSV transaction file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Normalize columns
            rename_map = {}
            if 'vendor' in df.columns: rename_map['vendor'] = 'vendor_name'
            if 'date' in df.columns: rename_map['date'] = 'transaction_date' 
            if 'type' in df.columns: rename_map['type'] = 'transaction_type'
            
            if rename_map:
                df = df.rename(columns=rename_map)
                
            with st.expander("🔎 Preview Raw Data", expanded=True):
                st.dataframe(df.head())
            
            if st.button("🚀 Ingest and Analyze", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 1. Ingestion
                status_text.markdown("### 📥 Ingesting data...")
                count = loader.ingest_dataframe(df)
                progress_bar.progress(30)
                st.success(f"✅ Ingested {count} new transactions into database.")
                
                # 2. Detection
                status_text.markdown("### 🕵️ Running detection pipeline...")
                findings = pipeline.run_all(df)
                progress_bar.progress(60)
                
                # Show statistical findings immediately
                if findings:
                    with st.expander(f"Found {len(findings)} Statistical Anomalies", expanded=True):
                        st.json([f['finding_summary'] for f in findings[:5]])
                        if len(findings) > 5: st.caption(f"...and {len(findings)-5} more")
                
                # 3. AI Enrichment
                status_text.markdown("### 🧠 Analyzing context with AI...")
                enriched_count = pipeline.enrich_with_ai()
                progress_bar.progress(90)
                st.success(f"✅ AI analyzed {enriched_count} anomalies.")
                
                progress_bar.progress(100)
                status_text.markdown("### 🎉 Analysis Complete!")
                
                st.balloons()
                st.info("👉 Check the **Dashboard** for trends or **Review Alerts** to take action.")

        except Exception as e:
            st.error(f"Error processing file: {e}")

elif selection == "Dashboard":
    show_dashboard()

elif selection == "Review Alerts":
    show_review()
