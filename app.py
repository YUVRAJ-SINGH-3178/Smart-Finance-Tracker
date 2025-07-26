import streamlit as st
import pandas as pd
import os
from datetime import datetime

# === Configuration ===
st.set_page_config(page_title="Smart Finance Tracker", layout="centered")
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# === Constants ===
DATA_FILE = "data/transactions.csv"
os.makedirs("data", exist_ok=True)

# === Initialize CSV ===
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df_init.to_csv(DATA_FILE, index=False)

# === Load Data ===
def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

df = load_data()

# === Add New Transaction ===
st.sidebar.header("➕ Add New Transaction")
with st.sidebar.form("entry_form", clear_on_submit=True):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Income", "Groceries", "Rent", "Bills", "Transport", "Entertainment", "Other"])
    amount = st.number_input("Amount (₹)", step=1.0, format="%.2f")
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        new_data = pd.DataFrame([[date, category, amount, description]], columns=df.columns)
        new_data.to_csv(DATA_FILE, mode="a", index=False, header=not os.path.exists(DATA_FILE))
        st.success("Transaction added!")
        st.experimental_rerun()

# === Reset Button ===
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Reset All Data"):
    df_empty = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df_empty.to_csv(DATA_FILE, index=False)
    st.warning("All data reset!")
    st.experimental_rerun()

# === Summary ===
st.title("📊 Smart Finance Tracker")

if df.empty:
    st.info("No transactions yet. Add some from the sidebar.")
else:
    income = df[df["Amount"] > 0]["Amount"].sum()
    expense = df[df["Amount"] < 0]["Amount"].sum()
    balance = income + expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"₹{income:,.2f}")
    col2.metric("Expense", f"₹{abs(expense):,.2f}")
    col3.metric("Balance", f"₹{balance:,.2f}")

    st.markdown("### 📜 Transaction History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

    # === Monthly Income Summary ===
    st.markdown("### 📆 Monthly Income Summary")

    income_df = df[df["Amount"] > 0].copy()
    if not income_df.empty:
        income_df["Month"] = income_df["Date"].dt.strftime("%B %Y")
        monthly_income = income_df.groupby("Month")["Amount"].sum().reset_index()
        monthly_income.columns = ["Month", "Total Income"]
        st.table(monthly_income)
    else:
        st.info("No income data available for monthly summary.")
