import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Import your prediction functions
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# -----------------------------------------------------------------------------
# Page Configuration (Must be the first Streamlit command)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Intelligent Invoicing Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Sidebar: Theme & Module Selection
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings & Navigation")
    
    # Custom Light/Dark Mode Toggle
    theme = st.radio("🎨 App Theme:", ["Auto (System)", "Light Mode", "Dark Mode"])
    
    if theme == "Dark Mode":
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {background-color: #121212;}
            [data-testid="stHeader"] {background-color: #121212;}
            [data-testid="stSidebar"] {background-color: #1E1E1E;}
            /* Force text colors to be light in Dark Mode */
            p, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown {color: #FAFAFA !important;}
            [data-testid="stMetricValue"] {color: #FAFAFA !important;}
        </style>
        """, unsafe_allow_html=True)
    elif theme == "Light Mode":
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {background-color: #FFFFFF;}
            [data-testid="stHeader"] {background-color: #FFFFFF;}
            [data-testid="stSidebar"] {background-color: #F0F2F6;}
            /* Force text colors to be dark in Light Mode */
            p, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown {color: #111111 !important;}
            [data-testid="stMetricValue"] {color: #111111 !important;}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    selected_model = st.radio(
        "🧠 Choose an AI Module:",
        ["Freight Cost Forecaster", "Invoice Risk Analyzer"]
    )
    
    st.markdown("---")
    st.markdown("### 📈 Business Impact")
    st.markdown("""
    - 🎯 **Accuracy:** Improve budgeting & forecasting.
    - 🛡️ **Security:** Instantly flag anomalies.
    - ⚡ **Speed:** Accelerate finance workflows.
    """)

# -----------------------------------------------------------------------------
# Header Section
# -----------------------------------------------------------------------------
st.title("🏢 Vendor Invoice Intelligence Portal")
st.markdown("Leveraging Machine Learning to optimize freight logistics and safeguard financial operations.")

st.info("""
**What this AI predicts:**
- 🚚 **Freight Costs:** Future shipping expenses based on invoice totals.
- 🚨 **Risk Flags:** High-probability anomalous invoices needing manual review.
- 📉 **Data Mismatches:** Discrepancies between expected POs and actual Invoices.
""")
st.divider()

# -----------------------------------------------------------------------------
# Module 1: Freight Cost Prediction
# -----------------------------------------------------------------------------
if selected_model == "Freight Cost Forecaster":
    st.subheader("🚚 Freight Cost Forecaster")
    
    st.markdown("""
    **Objective:** Predict expected freight costs instantly to support budgeting and vendor negotiations.
    
    **Input Field Guide:**
    * `💰 Invoice Value`: The total monetary amount requested by the vendor on the invoice.
    """)
    
    with st.form("freight_form"):
        dollars = st.number_input(
            "💰 Invoice Value (Dollars)", 
            min_value=1.0, 
            value=18500.0,
            step=100.0
        )
        
        submit_freight = st.form_submit_button("🔮 Predict Freight Cost", use_container_width=True)
        
    if submit_freight:
        input_data = {
            "Dollars": [dollars]
        }
        
        with st.spinner("Analyzing historical trends..."):
            prediction_df = predict_freight_cost(input_data)
            prediction_value = prediction_df['Predicted_Freight'][0]
            
        st.success("Prediction generated successfully!")
        st.metric(
            label="📊 Estimated Freight Cost", 
            value=f"${prediction_value:,.2f}"
        )

# -----------------------------------------------------------------------------
# Module 2: Invoice Risk Prediction
# -----------------------------------------------------------------------------
else:
    st.subheader("🚨 Invoice Risk Analyzer")
    
    st.markdown("""
    **Objective:** AI-powered evaluation to detect abnormal cost, freight, or delivery patterns.
    
    **Input Field Guide:**
    * `📦 Invoice Quantity`: Total items billed on the vendor's invoice.
    * `💵 Invoice Dollars`: Total monetary amount billed on the invoice.
    * `🚚 Freight Cost`: Shipping and handling charges applied.
    * `📋 Total Item Quantity`: Expected items based on the original Purchase Order.
    * `💰 Total Item Dollars`: Expected cost based on the original Purchase Order.
    """)
    
    with st.form("invoice_flag_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Invoice Details")
            invoice_quantity = st.number_input("📦 Invoice Quantity", min_value=1, value=50)
            invoice_dollars = st.number_input("💵 Invoice Dollars", min_value=1.0, value=352.95)
            freight = st.number_input("🚚 Freight Cost", min_value=0.0, value=1.73)
            
        with col2:
            st.markdown("#### Purchase Order (Item Level) Details")
            total_item_quantity = st.number_input("📋 Total Item Quantity", min_value=1, value=162)
            total_item_dollars = st.number_input("💰 Total Item Dollars", min_value=1.0, value=2476.0)
            
        st.markdown("<br>", unsafe_allow_html=True)
        submit_flag = st.form_submit_button("🛡️ Evaluate Invoice Risk", use_container_width=True)
        
    if submit_flag:
        input_data = {
            "invoice_quantity": [invoice_quantity],
            "invoice_dollars": [invoice_dollars],
            "Freight": [freight],
            "total_item_quantity": [total_item_quantity],
            "total_item_dollars": [total_item_dollars]
        }
        
        with st.spinner("Running anomaly detection..."):
            flag_prediction = predict_invoice_flag(input_data)['Predicted_Flag']
            is_flagged = bool(flag_prediction[0])
            
        if is_flagged:
            st.error("⚠️ **ALERT: High Risk Detected**")
            st.markdown("This invoice exhibits anomalous data patterns (e.g., severe price mismatches or abnormal delays) and requires **MANUAL APPROVAL**.")
        else:
            st.success("✅ **SAFE: Routine Invoice**")
            st.markdown("This invoice aligns with normal historical patterns and is safe for **Auto-Approval**.")