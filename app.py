import os
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="AI Expense Intelligence Platform", layout="wide")
st.title("📊 AI-Powered Enterprise Expense Tracker & Forecaster")
st.markdown("---")

@st.cache_data
def generate_and_clean_data():
    
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", periods=100, freq="D")
    categories = ["Food", "Rent", "Utilities", "Entertainment", "Travel"]
    
    data = {
        "Date": np.random.choice(dates, size=150),
        "Category": np.random.choice(categories, size=150),
        "Amount": np.random.choice([120, 500, -50, 1500, 4500, np.nan, 25000], size=150), # Missing and negative values included
        "Payment_Mode": np.random.choice(["UPI", "Credit Card", "Cash"], size=150)
    }
    df_messy = pd.DataFrame(data)
    

    df_clean = df_messy.dropna().copy() 
    df_clean = df_clean[df_clean["Amount"] > 0] 
    df_clean = df_clean[df_clean["Amount"] < 20000] 
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])
    df_clean = df_clean.sort_values("Date")
    
  
    conn = sqlite3.connect("expenses.db")
    df_clean.to_sql("clean_expenses", conn, if_exists="replace", index=False)
    conn.close()
    
    return df_clean

df = generate_and_clean_data()
st.sidebar.success("✅ AI Data Engine & SQLite Warehouse Online!")


selected_cat = st.sidebar.multiselect("Filter by Category", options=df["Category"].unique(), default=df["Category"].unique())
filtered_df = df[df["Category"].isin(selected_cat)]


total_spend = filtered_df["Amount"].sum()
avg_spend = filtered_df["Amount"].mean()
total_transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Capital Expenditure", f"₹ {total_spend:,.2f}")
col2.metric("📉 Average Transaction Cost", f"₹ {avg_spend:,.2f}")
col3.metric("🧾 Total Processed Invoices", f"{total_transactions}")
st.markdown("---")


chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Departmental Expense Distribution")
    cat_chart = px.pie(filtered_df, values="Amount", names="Category", hole=0.4, color_discrete_sequence=px.colors.sequential.Plotly3)
    st.plotly_chart(cat_chart, use_container_width=True)

with chart_col2:
    st.subheader("Transaction Volume by Payment Network")
    pay_chart = px.bar(filtered_df, x="Payment_Mode", y="Amount", color="Payment_Mode", barmode="group")
    st.plotly_chart(pay_chart, use_container_width=True)

st.markdown("---")

st.subheader("🔮 Predictive Analytics: Next Month Expense Forecasting (AI Layer)")


daily_trend = df.groupby("Date")["Amount"].sum().reset_index()
daily_trend['Day_Index'] = np.arange(len(daily_trend))

X = daily_trend['Day_Index']
Y = daily_trend['Amount']
slope, intercept = np.polyfit(X, Y, 1)


future_days = np.arange(len(daily_trend), len(daily_trend) + 30)
future_predictions = slope * future_days + intercept
future_dates = pd.date_range(start=daily_trend['Date'].max() + pd.Timedelta(days=1), periods=30)

forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Amount": future_predictions})


fig_forecast = px.line(daily_trend, x="Date", y="Amount", title="Historical Spend vs AI Predicted Trend")
fig_forecast.add_scatter(x=forecast_df["Date"], y=forecast_df["Predicted_Amount"], name="AI Next Month Forecast", mode="lines", line=dict(dash="dash", color="red"))
st.plotly_chart(fig_forecast, use_container_width=True)