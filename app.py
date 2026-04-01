import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")


st.title("🛍️ E-Commerce Customer Insights Dashboard")


@st.cache_data
def generate_data():
    np.random.seed(42)
    

    num_customers = 1000
    customers = pd.DataFrame({
        'customer_id': range(1, num_customers + 1),
        'age': np.random.randint(18, 70, num_customers),
        'gender': np.random.choice(['Male', 'Female'], num_customers),
        'location': np.random.choice(['Urban', 'Suburban', 'Rural'], num_customers)
    })
    
    # Orders data
    num_orders = 5000
    start_date = datetime(2023, 1, 1)
    orders = pd.DataFrame({
        'order_id': range(1, num_orders + 1),
        'customer_id': np.random.choice(customers['customer_id'], num_orders),
        'date': [start_date + timedelta(days=np.random.randint(0, 365*2)) for _ in range(num_orders)],
        'amount': np.random.exponential(50, num_orders) + 10
    })
    
    # Merge data
    data = orders.merge(customers, on='customer_id')
    return data, customers, orders

data, customers, orders = generate_data()

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"${data['amount'].sum():,.0f}")
with col2:
    st.metric("Total Orders", f"{len(data):,}")
with col3:
    st.metric("Total Customers", f"{len(customers):,}")
with col4:
    st.metric("Avg Order Value", f"${data['amount'].mean():.2f}")

st.divider()

# Revenue Trends
st.subheader("📈 Revenue Trends")
monthly_revenue = data.groupby(data['date'].dt.to_period('M'))['amount'].sum()
fig1, ax1 = plt.subplots(figsize=(14, 4))
ax1.plot(range(len(monthly_revenue)), monthly_revenue.values, marker='o', color='blue', linewidth=2, markersize=6)
ax1.set_title('Monthly Revenue Trends', fontsize=14, fontweight='bold')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue ($)')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(0, len(monthly_revenue), 3))
ax1.set_xticklabels([str(m) for m in monthly_revenue.index[::3]], rotation=45)
st.pyplot(fig1)

st.divider()

# Customer Demographics
st.subheader("👥 Customer Demographics")
col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.hist(customers['age'], bins=10, edgecolor='black', alpha=0.7, color='green')
    ax2.set_title('Customer Age Distribution', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Number of Customers')
    ax2.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig2)

with col2:
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    gender_counts = customers['gender'].value_counts()
    colors = ['#87CEEB', '#FFB6C1']
    ax3.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax3.set_title('Customer Gender Distribution', fontsize=12, fontweight='bold')
    st.pyplot(fig3)

st.divider()

# Purchasing Behavior
st.subheader("💳 Purchasing Behavior")
col1, col2, col3 = st.columns(3)

with col1:
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    ax4.hist(data['amount'], bins=20, edgecolor='black', alpha=0.7, color='orange')
    ax4.set_title('Purchase Amount Distribution', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Purchase Amount ($)')
    ax4.set_ylabel('Frequency')
    ax4.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig4)

with col2:
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    avg_purchase = data.groupby('customer_id')['amount'].mean()
    ax5.hist(avg_purchase, bins=15, edgecolor='black', alpha=0.7, color='purple')
    ax5.set_title('Avg Purchase per Customer', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Average Amount ($)')
    ax5.set_ylabel('Number of Customers')
    ax5.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig5)

with col3:
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    customer_stats = data.groupby('customer_id').agg({
        'amount': ['sum', 'count']
    }).reset_index()
    customer_stats.columns = ['customer_id', 'total_amount', 'frequency']
    ax6.scatter(customer_stats['frequency'], customer_stats['total_amount'], alpha=0.6, color='red', s=50)
    ax6.set_title('Frequency vs Total Amount', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Number of Purchases')
    ax6.set_ylabel('Total Amount Spent ($)')
    ax6.grid(True, alpha=0.3)
    st.pyplot(fig6)

st.divider()

# Additional Insights
st.subheader("📊 Additional Insights")
col1, col2 = st.columns(2)

with col1:
    st.write("**Location Distribution**")
    location_counts = customers['location'].value_counts()
    st.bar_chart(location_counts)

with col2:
    st.write("**Top 10 Customers by Total Spend**")
    top_customers = data.groupby('customer_id')['amount'].sum().nlargest(10).reset_index()
    top_customers.columns = ['Customer ID', 'Total Spend']
    st.dataframe(top_customers, use_container_width=True)

st.divider()
st.caption("Dashboard last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
