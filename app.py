import os
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="FinAI Platform", 
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def generate_and_clean_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", periods=150, freq="D")
    categories = ["Cloud Infrastructure", "Talent Acquisition", "Marketing Operations", "R&D Software", "Corporate Real Estate"]
    
    data = {
        "Date": np.random.choice(dates, size=250),
        "Category": np.random.choice(categories, size=250),
        "Amount": np.random.choice([3200, 7500, -250, 22000, 68000, np.nan, 850000], size=250),
        "Payment_Mode": np.random.choice(["Corporate Amex", "Wire Transfer", "ACH Invoicing"], size=250)
    }
    df_messy = pd.DataFrame(data)
    
    df_clean = df_messy.dropna().copy()
    df_clean = df_clean[df_clean["Amount"] > 0]
    df_clean = df_clean[df_clean["Amount"] < 200000] 
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])
    df_clean = df_clean.sort_values("Date")
    
    conn = sqlite3.connect("fin_intelligence.db")
    df_clean.to_sql("clean_expenses", conn, if_exists="replace", index=False)
    conn.close()
    return df_clean

df = generate_and_clean_data()

st.sidebar.title("Home")
page = st.sidebar.radio(
    label="Navigation Channels",
    options=[
        "📈 Expense's return comparison", 
        "🎲 Brownian simulation", 
        "📊 Portfolio dashboard", 
        "🔮 Forecast model"
    ],
    label_visibility="collapsed"
)

if page == "📈 Expense's return comparison":
    st.title("📈 Expense Distribution & Cost Allocation")
    st.caption("Detailed departmental expense structure and metric benchmarks.")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Capital Outlay", f"₹ {df['Amount'].sum():,.2f}")
    col2.metric("Avg Transaction Value", f"₹ {df['Amount'].mean():,.2f}")
    col3.metric("Total Invoices", f"{len(df)}")
    st.divider()
    
    fig_pie = px.pie(df, values="Amount", names="Category", hole=0.4, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_pie, use_container_width=True)

elif page == "🎲 Brownian simulation":
    st.title("🎲 Operational Anomalies & Outliers")
    st.caption("Identifying broken pipeline entries and non-conforming financial data points.")
    st.divider()
    
    fig_scatter = px.scatter(df, x="Date", y="Amount", color="Category", size="Amount", template="plotly_dark", title="Transaction Volatility Matrix")
    st.plotly_chart(fig_scatter, use_container_width=True)

elif page == "📊 Portfolio dashboard":
    st.title("📊 Enterprise SQL Ledger Database Warehouse")
    st.caption("Direct read access from the active local SQLite database layer.")
    st.divider()
    
    st.subheader("Query Output: SELECT * FROM clean_expenses")
    st.dataframe(df, use_container_width=True)

elif page == "🔮 Forecast model":
    st.title("🔮 Forecast model: ARIMA / Linear Regression")
    st.caption("Explore the future trajectory of the corporate expenses with this simple forecasting tool.")
    st.write("In this app, we used mathematical trendlines to forecast the next month's operation costs based on historical data.")
    st.write("Visualize the forecast alongside historical trends, gaining insights into potential market movements.")
    st.divider()
    
    st.subheader("S&P500 Price Forecasting App Clone (Expense Adaptation)")
    
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
    fig_forecast.update_traces(line=dict(color="#3b82f6", width=2.5), name="Historical Data")
    
    fig_forecast.add_scatter(
        x=forecast_df["Date"], 
        y=forecast_df["Predicted_Amount"], 
        name="Forecast", 
        mode="lines", 
        line=dict(color="#ff6b6b", width=3)
    )
    
    fig_forecast.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=10, r=10),
        xaxis=dict(showgrid=False, title="Time"),
        yaxis=dict(showgrid=True, gridcolor="#1f2937", title="Corporate Outlay Cost"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_forecast, use_container_width=True)