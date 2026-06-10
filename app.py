import os
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="FinAI // Global Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
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
    
    /* KPI Metric Cards with Neon Green Left Glow */
    div[data-testid="stMetric"] {
        background-color: #111827 !important;
        padding: 20px 25px !important;
        border-radius: 12px !important;
        border: 1px solid #1f2937 !important;
        border-left: 5px solid #10b981 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.15) !important;
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
    
    /* Divider Customization */
    hr { border-color: #1f2937 !important; }
    </style>
""", unsafe_allowed_html=True)


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
    
    
    df_clean = df_messy.dropna().copy()
    df_clean = df_clean[df_clean["Amount"] > 0]
    df_clean = df_clean[df_clean["Amount"] < 300000] # Cap outliers
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])
    df_clean = df_clean.sort_values("Date")
    
   
    conn = sqlite3.connect("fin_intelligence.db")
    df_clean.to_sql("clean_expenses", conn, if_exists="replace", index=False)
    conn.close()
    return df_clean

df = generate_and_clean_data()


st.sidebar.markdown("<h2 style='color:#ffffff; font-size:20px; margin-top:10px;'>System Environment</h2>", unsafe_allowed_html=True)
st.sidebar.markdown('<div class="status-badge">● AI PREDICTIVE CORE ONLINE</div>', unsafe_allowed_html=True)

st.sidebar.markdown("<hr>", unsafe_allowed_html=True)
st.sidebar.markdown("<h2 style='color:#ffffff; font-size:20px;'>Control Filters</h2>", unsafe_allowed_html=True)
selected_cat = st.sidebar.multiselect("Select Capital Cost Centers", options=df["Category"].unique(), default=df["Category"].unique())
filtered_df = df[df["Category"].isin(selected_cat)]


total_spend = filtered_df["Amount"].sum()
avg_spend = filtered_df["Amount"].mean()
total_transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)
with col1: st.metric("Total Capital Outlay", f"₹ {total_spend:,.2f}")
with col2: st.metric("Avg Transaction Value", f"₹ {avg_spend:,.2f}")
with col3: st.metric("Processed Ledger Invoices", f"{total_transactions}")

st.markdown("<br>", unsafe_allowed_html=True)

tab1, tab2 = st.tabs(["📊 Historical Analytics Ledger", "🔮 AI Predictive Intelligence Forecast"])

with tab1:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:15px;'>Cost Center Allocation</h3>", unsafe_allowed_html=True)
        cat_chart = px.pie(
            filtered_df, 
            values="Amount", 
            names="Category", 
            hole=0.55, 
            color_discrete_sequence=px.colors.sequential.Mint_r
        )
        cat_chart.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#ffffff",
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(cat_chart, use_container_width=True)
        
    with chart_col2:
        st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:15px;'>Vendor Settlement Networks</h3>", unsafe_allowed_html=True)
        pay_chart = px.bar(
            filtered_df, 
            x="Payment_Mode", 
            y="Amount", 
            color="Payment_Mode",
            color_discrete_sequence=["#10b981", "#34d399", "#059669"]
        )
        pay_chart.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#ffffff",
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="#1f2937", title="Total Amount")
        )
        st.plotly_chart(pay_chart, use_container_width=True)

with tab2:
    st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:5px;'>Advanced Predictive Modeling</h3>", unsafe_allowed_html=True)
    st.markdown("<p style='color:#9ca3af; font-size:14px; margin-bottom:20px;'>Linear trend forecast for the next 30 financial cycles based on running ledger averages.</p>", unsafe_allowed_html=True)
    
    
    daily_trend = df.groupby("Date")["Amount"].sum().reset_index()
    daily_trend['Day_Index'] = np.arange(len(daily_trend))

    X = daily_trend['Day_Index']
    Y = daily_trend['Amount']
    slope, intercept = np.polyfit(X, Y, 1)

    future_days = np.arange(len(daily_trend), len(daily_trend) + 30)
    future_predictions = slope * future_days + intercept
    future_dates = pd.date_range(start=daily_trend['Date'].max() + pd.Timedelta(days=1), periods=30)

    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Amount": future_predictions})


    fig_forecast = px.line(daily_trend, x="Date", y="Amount", title="")
    fig_forecast.update_traces(line=dict(color="#3b82f6", width=2.5), name="Historical Spend")
    
    fig_forecast.add_scatter(
        x=forecast_df["Date"], 
        y=forecast_df["Predicted_Amount"], 
        name="AI Target Trend Forecast", 
        mode="lines", 
        line=dict(dash="dash", color="#10b981", width=3)
    )
    
    fig_forecast.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#ffffff",
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1f2937"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_forecast, use_container_width=True)