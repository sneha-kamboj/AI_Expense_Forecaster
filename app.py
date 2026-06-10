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

st.title("📊 FinAI // Enterprise Expense Intelligence & Forecaster")
st.caption("Production Engine v2.5 • Predictive Financial Data Modeling Stack")
st.divider()

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
    df_clean = df_clean[df_clean["Amount"] < 300000] 
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])
    df_clean = df_clean.sort_values("Date")
    
    conn = sqlite3.connect("fin_intelligence.db")
    df_clean.to_sql("clean_expenses", conn, if_exists="replace", index=False)
    conn.close()
    return df_clean

df = generate_and_clean_data()

st.sidebar.title("Environment Panel")
st.sidebar.success("● AI PREDICTIVE CORE ONLINE")
st.sidebar.divider()

st.sidebar.subheader("Control Filters")
selected_cat = st.sidebar.multiselect("Select Capital Cost Centers", options=df["Category"].unique(), default=df["Category"].unique())
filtered_df = df[df["Category"].isin(selected_cat)]

total_spend = filtered_df["Amount"].sum()
avg_spend = filtered_df["Amount"].mean()
total_transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)
with col1: 
    st.metric(label="Total Capital Outlay", value=f"₹ {total_spend:,.2f}")
with col2: 
    st.metric(label="Avg Transaction Value", value=f"₹ {avg_spend:,.2f}")
with col3: 
    st.metric(label="Processed Ledger Invoices", value=f"{total_transactions}")

st.divider()

tab1, tab2 = st.tabs(["📊 Historical Analytics Ledger", "🔮 AI Predictive Intelligence Forecast"])

with tab1:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Cost Center Allocation")
        cat_chart = px.pie(
            filtered_df, 
            values="Amount", 
            names="Category", 
            hole=0.4, 
            color_discrete_sequence=px.colors.sequential.Mint_r,
            template="plotly_dark"
        )
        cat_chart.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        st.plotly_chart(cat_chart, use_container_width=True)
        
    with chart_col2:
        st.subheader("Vendor Settlement Networks")
        pay_chart = px.bar(
            filtered_df, 
            x="Payment_Mode", 
            y="Amount", 
            color="Payment_Mode",
            color_discrete_sequence=["#10b981", "#34d399", "#059669"],
            template="plotly_dark"
        )
        pay_chart.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(t=20, b=20, l=10, r=10),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, title="Total Amount")
        )
        st.plotly_chart(pay_chart, use_container_width=True)

with tab2:
    st.subheader("Advanced Predictive Modeling")
    st.caption("Linear trend forecast for the next 30 financial cycles based on running ledger averages.")
    
    daily_trend = df.groupby("Date")["Amount"].sum().reset_index()
    daily_trend['Day_Index'] = np.arange(len(daily_trend))

    X = daily_trend['Day_Index']
    Y = daily_trend['Amount']
    slope, intercept = np.polyfit(X, Y, 1)

    future_days = np.arange(len(daily_trend), len(daily_trend) + 30)
    future_predictions = slope * future_days + intercept
    future_dates = pd.date_range(start=daily_trend['Date'].max() + pd.Timedelta(days=1), periods=30)

    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Amount": future_predictions})

    fig_forecast = px.line(daily_trend, x="Date", y="Amount", template="plotly_dark")
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
        margin=dict(t=20, b=20, l=10, r=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_forecast, use_container_width=True)