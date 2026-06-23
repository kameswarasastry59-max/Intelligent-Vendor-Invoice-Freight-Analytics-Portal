🚀 Intelligent Vendor Invoice & Freight Analytics Portal

An end-to-end Machine Learning solution designed to optimize supply chain finances by accurately forecasting freight costs and automatically flagging anomalous vendor invoices for manual review.

Deployed as an interactive web application, this tool bridges the gap between raw database metrics and actionable business intelligence.

💼 Part 1: Business Context & Value

The project is divided into two core machine learning modules, each solving a distinct financial operations challenge:

1. Freight Cost Forecaster (Regression)

The Problem: Fluctuating shipping rates and unpredictable logistics costs make financial forecasting and budgeting incredibly difficult.

The Solution: A predictive model that estimates the expected freight cost based purely on the total monetary value of an invoice.

Business Impact: * Budgeting Precision: Allows the finance team to accurately lock in expected logistics costs before bills mature.

Vendor Negotiation: Empowers procurement teams to challenge vendors if the actual freight charged significantly exceeds the AI's predicted baseline.

2. Invoice Risk Analyzer (Classification)

The Problem: Manually auditing thousands of vendor invoices to find discrepancies (like price gouging, quantity mismatches, or extreme delivery delays) is time-consuming and prone to human error.

The Solution: An AI-driven classification engine that evaluates the relationship between the original Purchase Order (PO) and the final Vendor Invoice.

Business Impact:

Reduced Financial Leakage: Instantly catches over-billing and anomalous freight charges.

Operational Efficiency: Enables "Auto-Approval" for safe, routine invoices, allowing human auditors to focus 100% of their time on the high-risk invoices flagged by the model.

🧠 Part 2: Technical Deep Dive & Methodology

To ensure maximum accuracy and reliability, this project followed a rigorous, full-stack data science lifecycle—from raw SQL extraction to a deployed Streamlit application.

1. Data Engineering & Aggregation (SQLite & Pandas)

The raw data resided in a relational database containing separate tables for purchases (Purchase Orders) and vendor_invoice (Actual Bills).

Complex SQL CTEs: Built SQL queries to aggregate item-level purchase data up to the PO level (calculating total expected brands, quantities, and dollars).

Feature Extraction: Used SQL date math (Julian days) to engineer new features like days_po_to_invoice and avg_receiving_delay.

Data Merging: Executed Left Joins to perfectly align expected PO metrics with actual Invoice realities.

2. Feature Engineering & Deterministic Labeling

Because the dataset lacked a pre-existing "Fraud" target variable, a deterministic labeling function was engineered to create the Ground Truth (flag_invoice).
An invoice was flagged as risky (1) if:

The absolute difference between Expected PO Dollars and Actual Invoice Dollars exceeded a certain threshold.

The average receiving delay was highly abnormal (>10 days).

3. Exploratory Data Analysis (EDA) & Statistical Testing

Rather than blindly throwing data at an algorithm, rigorous statistical analysis was performed to validate feature importance.

Welch's T-Test: Utilized Welch's T-Test (equal_var=False) to mathematically prove that features like Freight had a statistically significant difference between "Normal" and "Risky" invoices, perfectly accounting for the massive variance and chaotic spread inherent to anomalous data.

4. Model Selection & Hyperparameter Tuning

The core classification task faced a common real-world problem: Class Imbalance (Normal invoices vastly outnumber Risky ones).

Baseline Models: Evaluated Logistic Regression and standard Decision Trees to establish a performance baseline.

Ensemble Learning: Selected a Random Forest Classifier as the champion model due to its robustness against overfitting and ability to capture non-linear relationships in financial data.

GridSearchCV Optimization: Instead of guessing the model configuration, deployed an exhaustive Grid Search over 216 unique hyperparameter combinations (n_estimators, max_depth, min_samples_split, criterion).

Custom Scoring: Crucially, the Grid Search was optimized specifically for the F1-Score using make_scorer. By maximizing the F1-Score rather than plain Accuracy, the model perfectly balances Precision (not crying wolf) and Recall (catching actual fraud).

5. Production Deployment (Streamlit)

The finalized, scaled models were serialized using joblib and deployed into a highly interactive, object-oriented Streamlit application.

Enterprise UI/UX: Features a sleek, modern interface with Custom Light/Dark mode toggles injected via CSS.

Real-time Inference: Users can input PO and Invoice metrics directly into the portal, which scales the data behind the scenes and returns an instantaneous Risk Evaluation or Freight Estimate.

🛠️ Technology Stack

Languages: Python, SQL (SQLite)

Data Processing: Pandas, NumPy, Scikit-Learn (StandardScaler)

Machine Learning: Scikit-Learn (RandomForestClassifier, GridSearchCV, f1_score)

Statistical Analysis: SciPy (Welch's T-Test)

Frontend/Deployment: Streamlit

Model Serialization: Joblib

💻 How to Run Locally

Follow these steps to run the Streamlit portal on your own machine:

1. Clone the Repository

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name


2. Install Dependencies
Ensure you have Python installed, then install the required packages:

pip install pandas numpy scikit-learn scipy plotly streamlit joblib


3. Run the Application
Launch the Streamlit app from your terminal:

streamlit run app.py


4. Access the Portal
Open your web browser and navigate to http://localhost:8501 to view the app!
