import os
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. PAGE SETUP (Premium Theme & Tab Title)
st.set_page_config(
    page_title="FinAI // Global Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED UI ENGINE (STRICT PYTHON STR VARIABLE FORMATTING) ---
custom_css = """
<style>
    /* Main Background & Text */
    .main { 
        background-color: #0b0f19 !important; 
        color: #f3f4f6 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Container Styling */
    .header-box {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #374151;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* KPI Metric Cards with Neon Glow */
    div[data-testid="stMetric"] {
        background-color: #111827 !important;
        padding: 20px 25px !important;
        border-radius: 12px !important;
        border: 1px solid #1f2937 !important;
        border-left: 5px solid #10b981 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Metric Typography */
    div[data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin-top: 5px;
    }

    /* Sidebar Customization */
    div[data-testid="stSidebar"] { 
        background-color: #0d111c !important; 
        border-right: 1px solid #1f2937;
    }
    
    /* Custom Sidebar Badges */
    .status-badge {
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.2);
        display: inline-block;
        margin-bottom: 20px;
    }

    /* Modern Streamlit Tabs Customization */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #9ca3af !important;
        background-color: transparent !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #10b981 !important;
        border-bottom: 3px solid #10b981 !important;
    }
    
    hr { border-color: #1f2937 !important; }
</style>
"""

# HTML injection using safe variable tracking
st.markdown(custom_css, unsafe_allowed_html=True)

# --- MAIN BRANDING HEADER ---
st.markdown("""
    <div class="header-box">
        <h1 style="margin:0; font-size:32px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">
            FinAI <span style="color:#10b981;">//</span> Enterprise Expense Intelligence & Forecaster
        </h1>
        <p style="margin:5px 0 0 0; color:#9ca3af; font-size:14px;">
            Production Engine v2.5 • Predictive Financial Data Modeling Stack
        </p>
    </div>
""", unsafe_allowed_html=True)

# 2. SETUP DATA ENGINE (Ingests and cleans data programmatically)
@st.cache_data
def generate_and_clean_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", periods=120, freq="D")
    categories = ["Cloud Infrastructure", "Talent Acquisition", "Marketing Operations", "R&D Software Pipelines", "Corporate Real Estate"]
    
    data = {
        "Date": np.random.choice(dates, size=200),
        "Category": np.random.choice(categories, size=200),
        "Amount": np.random.choice([3200, 7500, -250, 22000, 68000, np.nan, 850000], size=200),
        "Payment_Mode": np.random.choice(["Corporate Amex Platinum", "Cross-Border Wire Transfer", "ACH Automated Invoicing"], size=200)
    }
    df_messy = pd.DataFrame(data)
    
    # --- DATA ENGINEERING & PIPELINE LAYER ---
    df_clean = df_messy.dropna().copy()
    df_clean = df_clean[df_clean["Amount"] > 0]
    df_clean = df_clean[df_clean["Amount"] < 300000] # Cap outliers
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])
    df_clean = df_clean.sort_values("Date")
    
    # Save to SQLite Warehouse
    conn = sqlite3.connect("fin_intelligence.db")
    df_clean.to_sql("clean_expenses", conn, if_exists="replace", index=False)
    conn.close()
    return df_clean

df = generate_and_clean_data()

# --- SIDEBAR INTERFACE ---
st.sidebar.markdown("<h2 style='color:#ffffff; font-size:20px; margin-top:10px;'>System Environment</h2>", unsafe_allowed_html=True)
st.sidebar.markdown('<div class="status-badge">● AI PREDICTIVE CORE ONLINE</div>', unsafe_allowed_html=True)

st.sidebar.markdown("<hr>", unsafe_allowed_html=True)
st.sidebar.markdown("<h2 style='color:#ffffff; font-size:20px;'>Control Filters</h2>", unsafe_allowed_html=True)
selected_cat = st.sidebar.multiselect("Select Capital Cost Centers", options=df["Category"].unique(), default=df["Category"].unique())
filtered_df = df[df["Category"].isin(selected_cat)]

# 4. EXECUTIVE SCORECARDS
total_spend = filtered_df["Amount"].sum()
avg_spend = filtered_df["Amount"].mean()