"""
Sales Data Analysis Functions
Contains all data processing and analysis functions
"""

import pandas as pd
import numpy as np


# ==================== DATA LOADING ====================

def load_data():
    """
    Load sales data from CSV file
    
    Returns:
        DataFrame or None
    """
    try:
        # UTF-8 encoding
        df = pd.read_csv('data/superstore.csv', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            # latin-1 encoding
            df = pd.read_csv('data/superstore.csv', encoding='latin-1')
        except UnicodeDecodeError:
            try:
                # Windows-1252 encoding
                df = pd.read_csv('data/superstore.csv', encoding='cp1252')
            except:
                # Last resort - ignore errors
                df = pd.read_csv('data/superstore.csv', encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        return None
    
    # Convert date columns to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    return df


# ==================== OVERVIEW METRICS ====================

def get_overview_metrics(df):
    """
    Calculate key overview metrics
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        Dictionary with metrics
    """
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    return {
        'total_sales': round(total_sales, 2),
        'total_profit': round(total_profit, 2),
        'total_orders': total_orders,
        'total_customers': total_customers,
        'avg_order_value': round(avg_order_value, 2),
        'profit_margin': round(profit_margin, 2)
    }


# ==================== PRODUCT ANALYSIS ====================

def get_sales_by_category(df):
    """
    Get sales by category
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with category sales
    """
    category_sales = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    category_sales.columns = ['Category', 'Sales', 'Profit', 'Quantity', 'Orders']
    category_sales = category_sales.sort_values('Sales', ascending=False)
    
    return category_sales


def get_sales_by_subcategory(df, n=10):
    """
    Get top N sub-categories by sales
    
    Parameters:
        df: Sales DataFrame
        n: Number of top sub-categories
    
    Returns:
        DataFrame with sub-category sales
    """
    subcategory_sales = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    subcategory_sales.columns = ['Sub-Category', 'Sales', 'Profit', 'Quantity']
    subcategory_sales = subcategory_sales.sort_values('Sales', ascending=False).head(n)
    
    return subcategory_sales


def get_top_products(df, n=10):
    """
    Get top N products by sales
    
    Parameters:
        df: Sales DataFrame
        n: Number of top products
    
    Returns:
        DataFrame with top products
    """
    product_sales = df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    product_sales.columns = ['Product', 'Sales', 'Profit', 'Quantity']
    product_sales = product_sales.sort_values('Sales', ascending=False).head(n)
    
    return product_sales


# ==================== CUSTOMER ANALYSIS ====================

def get_sales_by_segment(df):
    """
    Get sales by customer segment
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with segment sales
    """
    segment_sales = df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    
    segment_sales.columns = ['Segment', 'Sales', 'Profit', 'Orders', 'Customers']
    segment_sales = segment_sales.sort_values('Sales', ascending=False)
    
    return segment_sales


def get_top_customers(df, n=10):
    """
    Get top N customers by sales
    
    Parameters:
        df: Sales DataFrame
        n: Number of top customers
    
    Returns:
        DataFrame with top customers
    """
    customer_sales = df.groupby('Customer Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    customer_sales.columns = ['Customer', 'Sales', 'Profit', 'Orders']
    customer_sales = customer_sales.sort_values('Sales', ascending=False).head(n)
    
    return customer_sales


# ==================== REGIONAL ANALYSIS ====================

def get_sales_by_region(df):
    """
    Get sales by region
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with regional sales
    """
    region_sales = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    
    region_sales.columns = ['Region', 'Sales', 'Profit', 'Orders', 'Customers']
    region_sales = region_sales.sort_values('Sales', ascending=False)
    
    return region_sales


def get_sales_by_state(df, n=10):
    """
    Get top N states by sales
    
    Parameters:
        df: Sales DataFrame
        n: Number of top states
    
    Returns:
        DataFrame with state sales
    """
    state_sales = df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    state_sales.columns = ['State', 'Sales', 'Profit', 'Orders']
    state_sales = state_sales.sort_values('Sales', ascending=False).head(n)
    
    return state_sales


def get_sales_by_city(df, n=10):
    """
    Get top N cities by sales
    
    Parameters:
        df: Sales DataFrame
        n: Number of top cities
    
    Returns:
        DataFrame with city sales
    """
    city_sales = df.groupby('City').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    city_sales.columns = ['City', 'Sales', 'Profit']
    city_sales = city_sales.sort_values('Sales', ascending=False).head(n)
    
    return city_sales


# ==================== TIME-BASED ANALYSIS ====================

def get_monthly_sales(df):
    """
    Get sales by month
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with monthly sales
    """
    df['Year-Month'] = df['Order Date'].dt.to_period('M')
    monthly_sales = df.groupby('Year-Month').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    monthly_sales.columns = ['Month', 'Sales', 'Profit', 'Orders']
    monthly_sales['Month'] = monthly_sales['Month'].astype(str)
    
    return monthly_sales


def get_yearly_sales(df):
    """
    Get sales by year
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with yearly sales
    """
    df['Year'] = df['Order Date'].dt.year
    yearly_sales = df.groupby('Year').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    yearly_sales.columns = ['Year', 'Sales', 'Profit', 'Orders']
    
    return yearly_sales


def get_quarterly_sales(df):
    """
    Get sales by quarter
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with quarterly sales
    """
    df['Quarter'] = df['Order Date'].dt.to_period('Q')
    quarterly_sales = df.groupby('Quarter').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    quarterly_sales.columns = ['Quarter', 'Sales', 'Profit']
    quarterly_sales['Quarter'] = quarterly_sales['Quarter'].astype(str)
    
    return quarterly_sales


# ==================== PROFITABILITY ANALYSIS ====================

def get_profit_by_category(df):
    """
    Get profitability metrics by category
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with profit analysis
    """
    profit_analysis = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    profit_analysis['Profit_Margin'] = (profit_analysis['Profit'] / profit_analysis['Sales'] * 100).fillna(0).round(2)
    profit_analysis = profit_analysis.sort_values('Profit', ascending=False)
    
    return profit_analysis


def get_most_profitable_products(df, n=10):
    """
    Get top N most profitable products
    
    Parameters:
        df: Sales DataFrame
        n: Number of products
    
    Returns:
        DataFrame with profitable products
    """
    product_profit = df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    product_profit.columns = ['Product', 'Sales', 'Profit']
    product_profit['Profit_Margin'] = (product_profit['Profit'] / product_profit['Sales'] * 100).fillna(0).round(2)
    product_profit = product_profit.sort_values('Profit', ascending=False).head(n)
    
    return product_profit


def get_loss_making_products(df, n=10):
    """
    Get top N loss-making products
    
    Parameters:
        df: Sales DataFrame
        n: Number of products
    
    Returns:
        DataFrame with loss-making products
    """
    product_profit = df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    product_profit.columns = ['Product', 'Sales', 'Profit']
    loss_products = product_profit[product_profit['Profit'] < 0]
    loss_products = loss_products.sort_values('Profit', ascending=True).head(n)
    
    return loss_products


# ==================== SHIPPING ANALYSIS ====================

def get_sales_by_ship_mode(df):
    """
    Get sales by shipping mode
    
    Parameters:
        df: Sales DataFrame
    
    Returns:
        DataFrame with shipping mode sales
    """
    ship_sales = df.groupby('Ship Mode').agg({
        'Sales': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    ship_sales.columns = ['Ship Mode', 'Sales', 'Orders']
    ship_sales = ship_sales.sort_values('Sales', ascending=False)
    
    return ship_sales


# ==================== UTILITY FUNCTIONS ====================

def get_unique_categories(df):
    """Get list of unique categories"""
    return sorted(df['Category'].unique().tolist())


def get_unique_regions(df):
    """Get list of unique regions"""
    return sorted(df['Region'].unique().tolist())


def get_unique_segments(df):
    """Get list of unique customer segments"""
    return sorted(df['Segment'].unique().tolist())


def get_date_range(df):
    """Get min and max dates from dataset"""
    return df['Order Date'].min(), df['Order Date'].max()