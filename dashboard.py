import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate synthetic data
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
    'amount': np.random.exponential(50, num_orders) + 10  # Exponential distribution for amounts
})

# Merge data
data = orders.merge(customers, on='customer_id')

# Create dashboard figure with subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('E-Commerce Customer Insights Dashboard', fontsize=16, fontweight='bold')

# 1. Revenue Trends - Monthly Revenue
monthly_revenue = data.groupby(data['date'].dt.to_period('M'))['amount'].sum()
axes[0, 0].plot(monthly_revenue.index.astype(str), monthly_revenue.values, marker='o', color='blue')
axes[0, 0].set_title('Monthly Revenue Trends')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Revenue ($)')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Customer Demographics - Age Distribution
axes[0, 1].hist(customers['age'], bins=10, edgecolor='black', alpha=0.7, color='green')
axes[0, 1].set_title('Customer Age Distribution')
axes[0, 1].set_xlabel('Age')
axes[0, 1].set_ylabel('Number of Customers')

# 3. Customer Demographics - Gender Distribution
gender_counts = customers['gender'].value_counts()
axes[0, 2].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'pink'])
axes[0, 2].set_title('Customer Gender Distribution')

# 4. Purchasing Behavior - Purchase Amount Distribution
axes[1, 0].hist(data['amount'], bins=20, edgecolor='black', alpha=0.7, color='orange')
axes[1, 0].set_title('Purchase Amount Distribution')
axes[1, 0].set_xlabel('Purchase Amount ($)')
axes[1, 0].set_ylabel('Frequency')

# 5. Purchasing Behavior - Average Purchase per Customer
avg_purchase = data.groupby('customer_id')['amount'].mean()
axes[1, 1].hist(avg_purchase, bins=15, edgecolor='black', alpha=0.7, color='purple')
axes[1, 1].set_title('Average Purchase per Customer')
axes[1, 1].set_xlabel('Average Amount ($)')
axes[1, 1].set_ylabel('Number of Customers')

# 6. Purchasing Behavior - Purchase Frequency vs Total Amount
customer_stats = data.groupby('customer_id').agg({
    'amount': ['sum', 'count']
}).reset_index()
customer_stats.columns = ['customer_id', 'total_amount', 'frequency']
axes[1, 2].scatter(customer_stats['frequency'], customer_stats['total_amount'], alpha=0.6, color='red')
axes[1, 2].set_title('Purchase Frequency vs Total Amount')
axes[1, 2].set_xlabel('Number of Purchases')
axes[1, 2].set_ylabel('Total Amount Spent ($)')

plt.tight_layout()
plt.savefig('ecommerce_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()