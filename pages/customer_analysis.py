"""
Customer Analysis Page
"""

import streamlit as st
import analysis as an

st.set_page_config(page_title="Customer Analysis", page_icon="👥", layout="wide")

# Load data
@st.cache_data
def load_data():
    return an.load_data()

df = load_data()

if df is None:
    st.error("⚠️ Data file not found!")
    st.stop()

# ==================== CUSTOMER ANALYSIS PAGE ====================

st.title("👥 Customer Analysis")

st.markdown("---")

# Customer Segments
st.markdown("## 📊 Customer Segments")

segment_sales = an.get_sales_by_segment(df)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales by Segment")
    chart_data = segment_sales.set_index('Segment')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Segment Details")
    st.dataframe(segment_sales, width='stretch', hide_index=True)

st.markdown("---")

# Top Customers
st.markdown("## 🌟 Top Customers")

# Number of customers to show
n_customers = st.slider("Number of Customers to Display", 5, 20, 10)

top_customers = an.get_top_customers(df, n=n_customers)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### Top {n_customers} Customers by Sales")
    chart_data = top_customers.set_index('Customer')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Customer Statistics")
    total_sales = top_customers['Sales'].sum()
    total_profit = top_customers['Profit'].sum()
    total_orders = top_customers['Orders'].sum()
    
    st.metric("Total Sales", f"${total_sales:,.0f}")
    st.metric("Total Profit", f"${total_profit:,.0f}")
    st.metric("Total Orders", f"{int(total_orders):,}")

# Top Customers Table
st.markdown("### Customer Details")
st.dataframe(top_customers, width='stretch', hide_index=True)

st.markdown("---")

# Segment Comparison
st.markdown("## 📈 Segment Performance Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Orders by Segment")
    chart_data = segment_sales.set_index('Segment')[['Orders']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Profit by Segment")
    chart_data = segment_sales.set_index('Segment')[['Profit']]
    st.bar_chart(chart_data)

with col3:
    st.markdown("### Customers by Segment")
    chart_data = segment_sales.set_index('Segment')[['Customers']]
    st.bar_chart(chart_data)

st.markdown("---")

# Segment Filter
st.markdown("## 🔍 Filter by Segment")

selected_segment = st.selectbox("Select Customer Segment", an.get_unique_segments(df))

if selected_segment:
    filtered_df = df[df['Segment'] == selected_segment]
    
    # Filtered metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
    with col2:
        st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
    with col3:
        st.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
    with col4:
        st.metric("Total Customers", f"{filtered_df['Customer ID'].nunique():,}")
    
    # Top customers in segment
    st.markdown(f"### Top 10 Customers in {selected_segment} Segment")
    filtered_customers = an.get_top_customers(filtered_df, n=10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_data = filtered_customers.set_index('Customer')[['Sales']]
        st.bar_chart(chart_data)
    
    with col2:
        st.dataframe(filtered_customers, width='stretch', hide_index=True)