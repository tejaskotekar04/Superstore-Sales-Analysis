"""
Sales Trends Page
"""

import streamlit as st
import analysis as an

st.set_page_config(page_title="Sales Trends", page_icon="📈", layout="wide")

# Load data
@st.cache_data
def load_data():
    return an.load_data()

df = load_data()

if df is None:
    st.error("⚠️ Data file not found!")
    st.stop()

# ==================== SALES TRENDS PAGE ====================

st.title("📈 Sales Trends Analysis")

st.markdown("---")

# Monthly Sales Trend
st.markdown("## 📅 Monthly Sales Trend")

monthly_sales = an.get_monthly_sales(df)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Sales & Profit Trend")
    chart_data = monthly_sales.set_index('Month')[['Sales', 'Profit']]
    st.line_chart(chart_data)

with col2:
    st.markdown("### Monthly Statistics")
    avg_monthly_sales = monthly_sales['Sales'].mean()
    avg_monthly_profit = monthly_sales['Profit'].mean()
    total_months = len(monthly_sales)
    
    st.metric("Avg Monthly Sales", f"${avg_monthly_sales:,.0f}")
    st.metric("Avg Monthly Profit", f"${avg_monthly_profit:,.0f}")
    st.metric("Total Months", total_months)

# Monthly Sales Table
st.markdown("### Monthly Sales Data")
st.dataframe(monthly_sales, width='stretch', hide_index=True)

st.markdown("---")

# Yearly Sales Trend
st.markdown("## 📆 Yearly Sales Trend")

yearly_sales = an.get_yearly_sales(df)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Yearly Sales")
    chart_data = yearly_sales.set_index('Year')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Yearly Profit")
    chart_data = yearly_sales.set_index('Year')[['Profit']]
    st.bar_chart(chart_data)

# Yearly Sales Table
st.markdown("### Yearly Performance Data")
st.dataframe(yearly_sales, width='stretch', hide_index=True)

st.markdown("---")

# Quarterly Sales Trend
st.markdown("## 📊 Quarterly Sales Trend")

quarterly_sales = an.get_quarterly_sales(df)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Quarterly Sales & Profit")
    chart_data = quarterly_sales.set_index('Quarter')[['Sales', 'Profit']]
    st.line_chart(chart_data)

with col2:
    st.markdown("### Quarterly Statistics")
    avg_quarterly_sales = quarterly_sales['Sales'].mean()
    avg_quarterly_profit = quarterly_sales['Profit'].mean()
    total_quarters = len(quarterly_sales)
    
    st.metric("Avg Quarterly Sales", f"${avg_quarterly_sales:,.0f}")
    st.metric("Avg Quarterly Profit", f"${avg_quarterly_profit:,.0f}")
    st.metric("Total Quarters", total_quarters)

# Quarterly Sales Table
st.markdown("### Quarterly Sales Data")
st.dataframe(quarterly_sales, width='stretch', hide_index=True)

st.markdown("---")

# Growth Analysis
st.markdown("## 📊 Growth Analysis")

if len(yearly_sales) > 1:
    # Calculate year-over-year growth
    yearly_sales_sorted = yearly_sales.sort_values('Year')
    yearly_sales_sorted['Sales_Growth'] = yearly_sales_sorted['Sales'].pct_change() * 100
    yearly_sales_sorted['Profit_Growth'] = yearly_sales_sorted['Profit'].pct_change() * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Year-over-Year Sales Growth")
        chart_data = yearly_sales_sorted.set_index('Year')[['Sales_Growth']]
        st.bar_chart(chart_data)
    
    with col2:
        st.markdown("### Year-over-Year Profit Growth")
        chart_data = yearly_sales_sorted.set_index('Year')[['Profit_Growth']]
        st.bar_chart(chart_data)
    
    st.markdown("### Growth Metrics")
    st.dataframe(yearly_sales_sorted, width='stretch', hide_index=True)
else:
    st.info("Need data from multiple years to show growth analysis")

st.markdown("---")

# Date Range Filter
st.markdown("## 🔍 Custom Date Range Analysis")

min_date, max_date = an.get_date_range(df)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)

with col2:
    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

if start_date and end_date:
    # Filter data by date range
    filtered_df = df[(df['Order Date'].dt.date >= start_date) & (df['Order Date'].dt.date <= end_date)]
    
    if len(filtered_df) > 0:
        # Display metrics for filtered period
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
        with col2:
            st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
        with col3:
            st.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
        with col4:
            profit_margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100) if filtered_df['Sales'].sum() > 0 else 0
            st.metric("Profit Margin", f"{profit_margin:.2f}%")
        
        # Show monthly trend for filtered period
        st.markdown("### Monthly Trend (Filtered Period)")
        filtered_monthly = an.get_monthly_sales(filtered_df)
        chart_data = filtered_monthly.set_index('Month')[['Sales', 'Profit']]
        st.line_chart(chart_data)
    else:
        st.warning("No data available for the selected date range")