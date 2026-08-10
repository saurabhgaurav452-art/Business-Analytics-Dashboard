import streamlit as st
import pandas as pd
import plotly.express as px
# pip install streamlit pandas plotly

st.set_page_config(page_title="Business Analytics Dashboard",
                   page_icon="📊",
                   layout="wide")

st.title("📊 Executive Business Analytics Dashboard")
st.markdown("Real-time Sales, Profit & Performance Insights")

df = pd.read_csv("data/sales_data.csv")

st.sidebar.title("📊 Dashboard Menu")

st.sidebar.info("""
Business Analytics Dashboard

Built with:
- Python
- Pandas
- Streamlit
- Plotly
""")

st.sidebar.header("Filters")

state = st.sidebar.selectbox(
    "Select State",
    ["All"] + list(df["State"].unique())
)

if state != "All":
    df = df[df["State"] == state]

# KPIs
total_sales = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].count()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", total_orders)

st.divider()

# Revenue by Category
st.subheader("Revenue by Category")

fig1 = px.bar(
    df.groupby("Category")["Revenue"].sum().reset_index(),
    x="Category",
    y="Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# Profit by Category
st.subheader("Profit by Category")

fig2 = px.pie(
    df,
    names="Category",
    values="Profit"
)

st.plotly_chart(fig2, use_container_width=True)

# City Sales
st.subheader("Sales by City")

fig3 = px.bar(
    df.groupby("City")["Revenue"].sum().reset_index(),
    x="City",
    y="Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

# Top Products

st.subheader("🏆 Top Products by Revenue")

top_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    title="Top Products Revenue"
)

st.plotly_chart(fig5, width="stretch")

st.download_button(
    label="📥 Download Sales Report",
    data=df.to_csv(index=False),
    file_name="sales_report.csv",
    mime="text/csv"
)

st.dataframe(df)

# Monthly Sales Trend

st.subheader("📈 Monthly Sales Trend")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

monthly_sales = (
    df.groupby(df["Order_Date"].dt.month)["Revenue"]
    .sum()
    .reset_index()
)

monthly_sales.columns = ["Month", "Revenue"]

fig4 = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig4, width="stretch")