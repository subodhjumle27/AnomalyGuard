# AnomalyGuard 🛡️

AI-powered data quality monitoring system for accounting and financial data.

## 🚀 The Problem
Accounting teams process thousands of transactions monthly. Manual sampling only catches **5% of errors**, leaving companies vulnerable to:
- 💸 **Duplicate payments** slipping through AP
- ⚠️ **Fraudulent patterns** in vendor spend
- 📉 **Inaccurate financial reporting** due to bad data

## 🛡️ The Solution
**AnomalyGuard** provides an automated, always-on surveillance layer. It combines **statistical rigor** with **AI context** to catch the 95% of issues manual reviews miss.

## ✨ Key Capabilities
- **Hybrid Detection Engine**:
  - 📊 **Statistical**: Z-score outliers, Benford's Law (planned), Duplicate checks
  - 🧠 **AI-Powered**: GPT-4.1 Nano analyzes transaction context (e.g., "Why is this Uber ride $500?")
  - ⏰ **Temporal**: Flags weekend/holiday activity and off-hours posting
- **Audit-Ready Workflow**: Full review interface with "Approve/Escalate" actions and persistent audit trails.


## 🛠️ Tech Stack
- **Framework**: Streamlit
- **AI**: OpenAI (GPT-4.1 Nano)
- **Database**: SQLite
- **Data**: Pandas, NumPy, SciPy

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd anomalyguard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_key_here
   ```

4. Initialize the database:
   ```bash
   python database/init_db.py
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```