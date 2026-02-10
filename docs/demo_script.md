# AnomalyGuard Demo Script

## 🎯 Scene 1: The Problem (30 seconds)
"Small and medium businesses often struggle with data quality in their accounting systems. Manual errors, duplicate entries, and unusual spending patterns often go unnoticed until it's too late — during a year-end audit."

## 🛡️ Scene 2: The Solution (30 seconds)
"AnomalyGuard is an AI-powered surveillance layer for financial data. It uses a hybrid approach: fast statistical checks for known patterns, and LLM-based contextual analysis for complex risks."

## 📊 Scene 3: The Demo (2 minutes)

### Part A: Ingestion
1. "Starting with the **Upload Data** page."
2. "I'll upload a CSV of 20 recent transactions." (Upload `samples/sample_transactions.csv`)
3. "The system immediately runs through our 6 detection modules."
4. "We found 12 potential anomalies. Let's see what they are."

### Part B: Dashboard
1. "Moving to the **Dashboard**."
2. "We can see our risk distribution: most are low risk, but we have 2 critical items."
3. "The bar chart shows that **DuplicateDetector** and **OutlierDetector** caught most of the issues."

### Part C: Human Review & AI Context
1. "Let's head over to the **Review Alerts** queue."
2. "Here's a critical item: Amazon for $150. The system flagged it as a duplicate."
3. "Notice the **✨ AI Context Analysis**: The LLM looked at the surrounding transactions and confirmed this matches a suspicious pattern often seen in double-billing errors."
4. "As a reviewer, I can look at the raw data, see the AI's reasoning, and either mark it as clean or escalate it."
5. "I'll mark this one as **Escalated** for further investigation."

## 📈 Scene 4: Conclusion (30 seconds)
"AnomalyGuard transforms a reactive audit process into a proactive quality control workflow. By catching these 12 items today, we've saved hours of manual reconciliation later and ensured data integrity for our clients."
