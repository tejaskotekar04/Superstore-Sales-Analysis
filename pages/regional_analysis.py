"""
Regional Analysis Page
"""

import streamlit as st
import analysis as an

st.set_page_config(page_title="Regional Analysis", page_icon="📍", layout="wide")

# Load data
@st.cache_data
def load_data():
    return an.load_data()

df = load_data()

if df is None:
    st.error("⚠️ Data file not found!")
    st.stop()

# ==================== REGIONAL ANALYSIS PAGE ====================

st.title("📍 Regional Analysis")

st.markdown("---")

# Regional Performance
st.markdown("## 🗺️ Sales by Region")

region_sales = an.get_sales_by_region(df)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales by Region")
    chart_data = region_sales.set_index('Region')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Profit by Region")
    chart_data = region_sales.set_index('Region')[['Profit']]
    st.bar_chart(chart_data)

# Regional Details Table
st.markdown("### Regional Performance Details")
st.dataframe(region_sales, width='stretch', hide_index=True)

st.markdown("---")

# State Analysis
st.markdown("## 🏛️ Sales by State")

# Number of states to show
n_states = st.slider("Number of States to Display", 5, 20, 10)

state_sales = an.get_sales_by_state(df, n=n_states)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### Top {n_states} States by Sales")
    chart_data = state_sales.set_index('State')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### State Statistics")
    total_sales = state_sales['Sales'].sum()
    total_profit = state_sales['Profit'].sum()
    total_orders = state_sales['Orders'].sum()
    
    st.metric("Total Sales", f"${total_sales:,.0f}")
    st.metric("Total Profit", f"${total_profit:,.0f}")
    st.metric("Total Orders", f"{int(total_orders):,}")

# State Details Table
st.markdown("### State Details")
st.dataframe(state_sales, width='stretch', hide_index=True)

st.markdown("---")

# City Analysis
st.markdown("## 🏙️ Sales by City")

# Number of cities to show
n_cities = st.slider("Number of Cities to Display", 5, 20, 10, key='cities_slider')

city_sales = an.get_sales_by_city(df, n=n_cities)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### Top {n_cities} Cities by Sales")
    chart_data = city_sales.set_index('City')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### City Details")
    st.dataframe(city_sales, width='stretch', hide_index=True)

st.markdown("---")

# Region Filter
st.markdown("## 🔍 Filter by Region")

selected_region = st.selectbox("Select Region", an.get_unique_regions(df))

if selected_region:
    filtered_df = df[df['Region'] == selected_region]
    
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
    
    st.markdown(f"### Performance in {selected_region} Region")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top states in region
        st.markdown("#### Top States")
        region_states = an.get_sales_by_state(filtered_df, n=10)
        chart_data = region_states.set_index('State')[['Sales']]
        st.bar_chart(chart_data)
    
    with col2:
        # Top cities in region
        st.markdown("#### Top Cities")
        region_cities = an.get_sales_by_city(filtered_df, n=10)
        chart_data = region_cities.set_index('City')[['Sales']]
        st.bar_chart(chart_data)
    
    # Category performance in region
    st.markdown(f"#### Category Performance in {selected_region}")
    region_category = an.get_sales_by_category(filtered_df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_data = region_category.set_index('Category')[['Sales']]
        st.bar_chart(chart_data)
    
    with col2:
        st.dataframe(region_category, width='stretch', hide_index=True)