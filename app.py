import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Load or create transactions.csv
DATA_FILE = 'data/transactions.csv'

if not os.path.exists(DATA_FILE):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

# App layout
st.set_page_config(page_title="Smart Finance Tracker", layout="centered")

st.title("💰 Smart Finance Tracker")
st.markdown("Track your income and expenses easily. Add a transaction below:")

# Input form
with st.form(key='transaction_form'):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", value=datetime.today())
        amount = st.number_input("Amount (₹)", format="%.2f", step=1.0)
    with col2:
        description = st.text_input("Description")
        category = st.selectbox("Category", ["Food", "Transport", "Bills", "Salary", "Shopping", "Others"])
    
    submit = st.form_submit_button("➕ Add Transaction")

if submit:
    new_data = {
        "Date": date.strftime("%Y-%m-%d"),
        "Description": description,
        "Amount": amount,
        "Category": category
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Transaction added successfully!")

# Display existing data
st.subheader("📋 Transaction History")
st.dataframe(df, use_container_width=True)

# Category-wise summary
if not df.empty:
    st.subheader("📊 Spending by Category")
    category_summary = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_summary)

    st.subheader("🧾 Total Summary")
    income = df[df["Amount"] > 0]["Amount"].sum()
    expense = df[df["Amount"] < 0]["Amount"].sum()
    balance = income + expense

    st.markdown(f"""
    - ✅ **Total Income:** ₹{income:.2f}  
    - ❌ **Total Expenses:** ₹{abs(expense):.2f}  
    - 💼 **Balance:** ₹{balance:.2f}
    """)
else:
    st.info("No transactions yet. Add some using the form above.")

