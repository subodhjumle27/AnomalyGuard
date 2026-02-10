import pandas as pd
from detectors import DetectionPipeline
from utils.data_loader import DataLoader
import os

# Initialize
loader = DataLoader()
pipeline = DetectionPipeline()

# Load sample
csv_path = 'samples/sample_with_anomalies.csv'
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found")
    exit(1)

df = pd.read_csv(csv_path)
print("Original Columns:", df.columns.tolist())

# Normalize columns (mimicking app.py logic)
rename_map = {}
if 'vendor' in df.columns: rename_map['vendor'] = 'vendor_name'
if 'date' in df.columns: rename_map['date'] = 'transaction_date' 
if 'type' in df.columns: rename_map['type'] = 'transaction_type'

if rename_map:
    df = df.rename(columns=rename_map)
    print("Renamed Columns:", df.columns.tolist())

# Ingest
print("Ingesting...")
count = loader.ingest_dataframe(df)
print(f"Ingested {count} rows.")

# Run Pipeline
print("Running Detection Pipeline...")
try:
    findings = pipeline.run_all(df)
    print(f"Success! Found {len(findings)} anomalies.")
    for f in findings:
        print(f" - [{f['detector_name']}] {f['finding_summary']}")
except Exception as e:
    print(f"Pipeline Failed: {e}")
    import traceback
    traceback.print_exc()

# Run AI Enrichment
print("\nRunning AI Enrichment...")
try:
    enriched_count = pipeline.enrich_with_ai()
    print(f"Success! Enriched {enriched_count} anomalies.")
except Exception as e:
    print(f"AI Enrichment Failed: {e}")
    import traceback
    traceback.print_exc()
