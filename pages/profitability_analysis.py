"""
Profitability Analysis Page
"""

import streamlit as st
import analysis as an

st.set_page_config(page_title="Profitability Analysis", page_icon="💰", layout="wide")

# Load data
@st.cache_data
def load_data():
    return an.load_data()

df = load_data()

if df is None:
    st.error("⚠️ Data file not found!")
    st.stop()

# ==================== PROFITABILITY ANALYSIS PAGE ====================

st.title("💰 Profitability Analysis")

st.markdown("---")

# Overall Profitability Metrics
st.markdown("## 📊 Overall Profitability")

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_loss = df[df['Profit'] < 0]['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${total_sales:,.0f}")
with col2:
    st.metric("Total Profit", f"${total_profit:,.0f}")
with col3:
    st.metric("Total Loss", f"${total_loss:,.0f}")
with col4:
    st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# Profit by Category
st.markdown("## 📦 Profitability by Category")

profit_by_category = an.get_profit_by_category(df)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Profit by Category")
    chart_data = profit_by_category.set_index('Category')[['Profit']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Profit Margin by Category")
    chart_data = profit_by_category.set_index('Category')[['Profit_Margin']]
    st.bar_chart(chart_data)

# Category Profitability Table
st.markdown("### Category Profitability Details")
st.dataframe(profit_by_category, width='stretch', hide_index=True)

st.markdown("---")

# Most Profitable Products
st.markdown("## 🌟 Most Profitable Products")

n_products = st.slider("Number of Products to Display", 5, 20, 10)

profitable_products = an.get_most_profitable_products(df, n=n_products)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### Top {n_products} Most Profitable Products")
    chart_data = profitable_products.set_index('Product')[['Profit']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Profitability Statistics")
    total_profit = profitable_products['Profit'].sum()
    total_sales = profitable_products['Sales'].sum()
    avg_margin = profitable_products['Profit_Margin'].mean()
    
    st.metric("Total Profit", f"${total_profit:,.0f}")
    st.metric("Total Sales", f"${total_sales:,.0f}")
    st.metric("Avg Profit Margin", f"{avg_margin:.2f}%")

# Profitable Products Table
st.markdown("### Product Details")
st.dataframe(profitable_products, width='stretch', hide_index=True)

st.markdown("---")

# Loss-Making Products
st.markdown("## ⚠️ Loss-Making Products")

n_loss_products = st.slider("Number of Loss Products to Display", 5, 20, 10, key='loss_slider')

loss_products = an.get_loss_making_products(df, n=n_loss_products)

if len(loss_products) > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### Top {n_loss_products} Loss-Making Products")
        chart_data = loss_products.set_index('Product')[['Profit']]
        st.bar_chart(chart_data)
    
    with col2:
        st.markdown("### Loss Statistics")
        total_loss = loss_products['Profit'].sum()
        total_sales_loss = loss_products['Sales'].sum()
        
        st.metric("Total Loss", f"${total_loss:,.0f}")
        st.metric("Sales Generated", f"${total_sales_loss:,.0f}")
        st.metric("Number of Products", len(loss_products))
    
    # Loss Products Table
    st.markdown("### Loss-Making Product Details")
    st.dataframe(loss_products, width='stretch', hide_index=True)
    
    st.warning("⚠️ These products are generating losses. Consider reviewing pricing or discontinuing them.")
else:
    st.success("✅ No loss-making products found! All products are profitable.")

st.markdown("---")

# Shipping Mode Analysis
st.markdown("## 🚚 Profitability by Shipping Mode")

ship_mode_sales = an.get_sales_by_ship_mode(df)

# Calculate profit by shipping mode
ship_mode_profit = df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

ship_mode_profit['Profit_Margin'] = (ship_mode_profit['Profit'] / ship_mode_profit['Sales'] * 100).fillna(0).round(2)
ship_mode_profit = ship_mode_profit.sort_values('Profit', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Profit by Shipping Mode")
    chart_data = ship_mode_profit.set_index('Ship Mode')[['Profit']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Shipping Mode Details")
    st.dataframe(ship_mode_profit, width='stretch', hide_index=True)