import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

st.set_page_config(page_title="Smart Finance Tracker", layout="centered")

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "transactions.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize empty CSV if it doesn't exist
if not os.path.isfile(DATA_FILE):
    pd.DataFrame(columns=["Date", "Category", "Amount", "Type"]).to_csv(DATA_FILE, index=False)

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df = df.dropna(subset=["Date"])
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])

def save_data(new_data):
    df = load_data()
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def reset_data():
    pd.DataFrame(columns=["Date", "Category", "Amount", "Type"]).to_csv(DATA_FILE, index=False)

st.title("💰 Smart Finance Tracker")

# --- Add Transaction Section ---
st.header("➕ Add Transaction")
with st.form("entry_form", clear_on_submit=True):
    date = st.date_input("Date", datetime.now().date())
    category = st.text_input("Category (e.g., Salary, Groceries)")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    trans_type = st.selectbox("Type", ["Income", "Expense"])
    submitted = st.form_submit_button("Add Transaction")

if submitted:
    if category and amount:
        new_entry = pd.DataFrame([{
            "Date": pd.to_datetime(date),
            "Category": category,
            "Amount": amount,
            "Type": trans_type
        }])
        save_data(new_entry)
        st.success(f"{trans_type} of ₹{amount} added!")
    else:
        st.error("Please fill all fields!")

# --- Reset Button ---
if st.button("🔄 Reset All Data"):
    reset_data()
    st.success("All data has been reset!")

# --- Load & Show Data ---
df = load_data()
if df.empty:
    st.info("No transactions yet.")
else:
    st.subheader("📊 Transaction History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

    # Summary
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expenses = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expenses

    st.metric("Total Income", f"₹{income:,.2f}")
    st.metric("Total Expenses", f"₹{expenses:,.2f}")
    st.metric("Net Balance", f"₹{balance:,.2f}")

    # Monthly Income Summary
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_income = df[df["Type"] == "Income"].groupby("Month")["Amount"].sum()

    st.subheader("📅 Monthly Income Summary")
    st.bar_chart(monthly_income)

