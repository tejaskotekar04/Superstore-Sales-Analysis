"""
Product Analysis Page
"""

import streamlit as st
import analysis as an

st.set_page_config(page_title="Product Analysis", page_icon="📦", layout="wide")

# Load data
@st.cache_data
def load_data():
    return an.load_data()

df = load_data()

if df is None:
    st.error("⚠️ Data file not found!")
    st.stop()

# ==================== PRODUCT ANALYSIS PAGE ====================

st.title("📦 Product Analysis")

st.markdown("---")

# Category Performance
st.markdown("## 🏷️ Category Performance")

category_sales = an.get_sales_by_category(df)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales by Category")
    chart_data = category_sales.set_index('Category')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Profit by Category")
    chart_data = category_sales.set_index('Category')[['Profit']]
    st.bar_chart(chart_data)

# Category Details Table
st.markdown("### Category Details")
st.dataframe(category_sales, width='stretch', hide_index=True)

st.markdown("---")

# Sub-Category Analysis
st.markdown("## 📋 Sub-Category Analysis")

# Number of sub-categories to show
n_subcategories = st.slider("Number of Sub-Categories to Display", 5, 20, 10)

subcategory_sales = an.get_sales_by_subcategory(df, n=n_subcategories)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### Top {n_subcategories} Sub-Categories by Sales")
    chart_data = subcategory_sales.set_index('Sub-Category')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Sub-Category Details")
    st.dataframe(subcategory_sales, width='stretch', hide_index=True)

st.markdown("---")

# Top Products
st.markdown("## 🌟 Top Products")

# Number of products to show
n_products = st.slider("Number of Products to Display", 5, 20, 10, key='products_slider')

top_products = an.get_top_products(df, n=n_products)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### Top {n_products} Products by Sales")
    chart_data = top_products.set_index('Product')[['Sales']]
    st.bar_chart(chart_data)

with col2:
    st.markdown("### Product Statistics")
    total_sales = top_products['Sales'].sum()
    total_profit = top_products['Profit'].sum()
    total_quantity = top_products['Quantity'].sum()
    
    st.metric("Total Sales", f"${total_sales:,.0f}")
    st.metric("Total Profit", f"${total_profit:,.0f}")
    st.metric("Total Quantity", f"{int(total_quantity):,}")

# Top Products Table
st.markdown("### Product Details")
st.dataframe(top_products, width='stretch', hide_index=True)

st.markdown("---")

# Category Filter
st.markdown("## 🔍 Filter by Category")

selected_category = st.selectbox("Select Category", an.get_unique_categories(df))

if selected_category:
    filtered_df = df[df['Category'] == selected_category]
    
    # Filtered metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
    with col2:
        st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
    with col3:
        st.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
    with col4:
        st.metric("Total Quantity", f"{int(filtered_df['Quantity'].sum()):,}")
    
    # Sub-categories in selected category
    st.markdown(f"### Sub-Categories in {selected_category}")
    filtered_subcategory = an.get_sales_by_subcategory(filtered_df, n=20)
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_data = filtered_subcategory.set_index('Sub-Category')[['Sales']]
        st.bar_chart(chart_data)
    
    with col2:
        st.dataframe(filtered_subcategory, width='stretch', hide_index=True)