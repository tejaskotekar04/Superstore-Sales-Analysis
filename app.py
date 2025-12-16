"""
Superstore Sales Analysis Dashboard
Main Application - Home Page
"""

import streamlit as st
import analysis as an

# Page Configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data (cached)
@st.cache_data
def load_data():
    """Load and cache sales data"""
    return an.load_data()

# Load the data
df = load_data()

# Check if data is loaded
if df is None:
    st.error("⚠️ **Error: Data file not found!**")
    st.info("""
    Please place your Superstore CSV file in the `data/` folder:
    - `data/superstore.csv`
    """)
    st.stop()

# ==================== HOME PAGE ====================

st.title("📊 Superstore Sales Analysis Dashboard")
st.markdown("### Comprehensive Sales Analytics & Insights")

st.markdown("---")

# Get overview metrics
metrics = an.get_overview_metrics(df)

# Display Key Metrics
st.markdown("## 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${metrics['total_sales']:,.0f}",
        help="Total revenue from all orders"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${metrics['total_profit']:,.0f}",
        help="Total profit earned"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{metrics['total_orders']:,}",
        help="Number of unique orders"
    )

with col4:
    st.metric(
        "Total Customers",
        f"{metrics['total_customers']:,}",
        help="Number of unique customers"
    )

# Second row of metrics
col5, col6 = st.columns(2)

with col5:
    st.metric(
        "Average Order Value",
        f"${metrics['avg_order_value']:,.2f}",
        help="Average revenue per order"
    )

with col6:
    st.metric(
        "Profit Margin",
        f"{metrics['profit_margin']:.2f}%",
        help="Overall profit margin percentage"
    )

st.markdown("---")

# Sales Overview Charts
st.markdown("## 📊 Sales Overview")

col1, col2 = st.columns(2)

with col1:
    # Sales by Category
    st.markdown("### Sales by Category")
    category_sales = an.get_sales_by_category(df)
    chart_data = category_sales.set_index('Category')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    # Sales by Region
    st.markdown("### Sales by Region")
    region_sales = an.get_sales_by_region(df)
    chart_data = region_sales.set_index('Region')[['Sales']]
    st.bar_chart(chart_data)

st.markdown("---")

# Sales by Customer Segment
st.markdown("### Sales by Customer Segment")
segment_sales = an.get_sales_by_segment(df)
chart_data = segment_sales.set_index('Segment')[['Sales']]
st.bar_chart(chart_data)

st.markdown("---")

# Monthly Sales Trend
st.markdown("### Monthly Sales Trend")
monthly_sales = an.get_monthly_sales(df)
chart_data = monthly_sales.set_index('Month')[['Sales', 'Profit']]
st.line_chart(chart_data)

st.markdown("---")

# Quick Data Summary
st.markdown("## 📋 Dataset Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Dataset Information:**")
    st.write(f"- Total Records: {len(df):,}")
    st.write(f"- Date Range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
    st.write(f"- Categories: {df['Category'].nunique()}")
    st.write(f"- Sub-Categories: {df['Sub-Category'].nunique()}")

with col2:
    st.markdown("**Geographic Coverage:**")
    st.write(f"- Regions: {df['Region'].nunique()}")
    st.write(f"- States: {df['State'].nunique()}")
    st.write(f"- Cities: {df['City'].nunique()}")
    st.write(f"- Customer Segments: {df['Segment'].nunique()}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Superstore Sales Dashboard | Built with Streamlit, Pandas, and NumPy</p>
    <p>Use the sidebar to navigate to different analysis pages →</p>
</div>
""", unsafe_allow_html=True)