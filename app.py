import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

# Page setup
st.set_page_config(page_title="Smart Finance Tracker", page_icon="💰")

# Sidebar
with st.sidebar:
    st.markdown("### 👋 About")
    st.markdown("This is a simple personal finance tracker app built using Streamlit.")
    st.markdown("Made by Yuvie 💻")
    st.markdown("---")
    st.markdown("📅 Track your expenses monthly\n💡 Add notes\n📊 View total spending per month")

# Main title
st.title("💰 Smart Finance Tracker")

# --- Input Section ---
st.markdown("## 💳 Add New Transaction")

col1, col2 = st.columns(2)

with col1:
    date_input = st.date_input("Date", value=date.today())
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")

with col2:
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Other"])
    note = st.text_input("Note (optional)")

if st.button("➕ Add Transaction"):
    new_data = {
        "Date": [str(date_input)],
        "Category": [category],
        "Amount": [amount],
        "Note": [note if note else "None"]
    }

    new_df = pd.DataFrame(new_data)

    file_path = "data/transactions.csv"
    os.makedirs("data", exist_ok=True)

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    updated_df.to_csv(file_path, index=False)
    st.success("Transaction added successfully!")

# --- Transaction History ---
st.markdown("## 📊 Transaction History")

file_path = "data/transactions.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df, use_container_width=True)

    # Process for chart
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_sum = df.groupby("Month")["Amount"].sum()

    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    monthly_sum.plot(kind="bar", ax=ax, color="skyblue")
    plt.xticks(rotation=45)
    ax.set_ylabel("₹ Spent")
    ax.set_title("Monthly Expense Summary")
    st.pyplot(fig)
else:
    st.info("No transactions found yet. Add your first one above! ✅")
