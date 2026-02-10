import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

def show_dashboard(db_path='anomalyguard.db'):
    st.header("📊 Anomaly Dashboard")
    
    conn = sqlite3.connect(db_path)
    df_all = pd.read_sql_query("SELECT * FROM monitored_transactions", conn)
    df_anomalies = pd.read_sql_query("SELECT * FROM anomaly_detections", conn)
    conn.close()
    
    if df_all.empty:
        st.warning("No data found. Please upload a file first.")
        return

    st.markdown("""
    **Real-time view of your data health.** Monitor flagged risks, detection categories, and review progress.
    """)

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", len(df_all))
    with col2:
        flagged_count = len(df_all[df_all['status'] == 'flagged'])
        st.metric("Flagged Anomalies", flagged_count)
    with col3:
        critical_count = len(df_all[df_all['risk_level'] == 'critical'])
        st.metric("Critical Risks", critical_count)
    with col4:
        reviewed_count = len(df_all[df_all['status'].isin(['reviewed', 'escalated'])])
        st.metric("Reviewed", reviewed_count)

    # Charts
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Risk Distribution")
        risk_counts = df_all['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        # Define colors for risk levels
        color_map = {'critical': '#d62728', 'high': '#ff7f0e', 'medium': '#fcf655', 'low': '#2ca02c'}
        fig = px.pie(risk_counts, values='Count', names='Risk Level', 
                     color='Risk Level', color_discrete_map=color_map, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("Anomalies by Detector")
        if not df_anomalies.empty:
            det_counts = df_anomalies['detector_name'].value_counts().reset_index()
            det_counts.columns = ['Detector', 'Count']
            fig = px.bar(det_counts, x='Detector', y='Count', color='Detector')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No anomaly detections to display.")

    st.subheader("Priority Queue (Filtered Flagged Transactions)")
    priority_df = df_all[df_all['status'] == 'flagged'].sort_values(by='risk_level', ascending=False)
    if not priority_df.empty:
        st.dataframe(priority_df[['transaction_id', 'transaction_date', 'amount', 'vendor_name', 'risk_level', 'status']])
    else:
        st.success("All caught up! No flagged transactions needing review.")
