import streamlit as st
import pandas as pd
import sqlite3
import json

def show_review(db_path='anomalyguard.db'):
    st.header("🔍 Alert Review Queue")
    
    conn = sqlite3.connect(db_path)
    # Get all flagged transactions and their detections
    query = """
    SELECT mt.*, ad.id as detection_id, ad.detector_name, ad.finding_summary, ad.finding_details_json, ad.llm_context_analysis, ad.llm_risk_assessment, ad.combined_risk_score
    FROM monitored_transactions mt
    JOIN anomaly_detections ad ON mt.transaction_id = ad.transaction_id
    WHERE mt.status = 'flagged'
    ORDER BY ad.combined_risk_score DESC
    """
    df_review = pd.read_sql_query(query, conn)
    conn.close()
    
    if df_review.empty:
        st.success("No flagged transactions to review!")
        return

    st.write(f"Showing {len(df_review)} items needing review.")
    
    # Review Interface
    for idx, row in df_review.iterrows():
        with st.expander(f"[{row['risk_level'].upper()}] {row['vendor_name']} - ${row['amount']} ({row['finding_summary']})", expanded=(idx == 0)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Transaction Details")
                st.json(json.loads(row['data_json']))
                
            with col2:
                st.markdown("#### Detection Context")
                st.info(f"**Detector:** {row['detector_name']}")
                st.write(f"**Summary:** {row['finding_summary']}")
                
                if row['llm_context_analysis']:
                    st.markdown("---")
                    st.markdown("#### ✨ AI Context Analysis")
                    st.write(row['llm_context_analysis'])
                    st.markdown(f"**AI Risk Level:** {row['llm_risk_assessment']}")
                
            st.markdown("---")
            action_col1, action_col2, action_col3 = st.columns(3)
            
            with action_col3:
                notes = st.text_input("Review Notes", key=f"notes_{row['detection_id']}")
                
            with action_col1:
                if st.button("Mark as Clean", key=f"clean_{row['detection_id']}"):
                    update_status(row['transaction_id'], row['detection_id'], 'clean', notes, db_path)
                    st.rerun()
                    
            with action_col2:
                if st.button("Escalate to Manager", key=f"esc_{row['detection_id']}"):
                    update_status(row['transaction_id'], row['detection_id'], 'escalated', notes, db_path)
                    st.rerun()

def update_status(txn_id, det_id, new_status, notes, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update transaction status
    cursor.execute("UPDATE monitored_transactions SET status = ? WHERE transaction_id = ?", (new_status, txn_id))
    
    # Add to review_actions audit trail
    cursor.execute("""
        INSERT INTO review_actions (transaction_id, detection_id, action_type, reviewer, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (txn_id, det_id, new_status, 'user', notes))
    
    conn.commit()
    conn.close()
    st.success(f"Transaction {txn_id} marked as {new_status}.")
