"""
Sales Data Visualization Functions
Contains all chart and visualization functions using Streamlit
"""

import streamlit as st

def show_sales_chart(data, x_col, y_col, title="Sales Chart"):
    """
    Display a bar chart
    
    Parameters:
        data: DataFrame
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
    """
    st.markdown(f"### {title}")
    chart_data = data.set_index(x_col)[[y_col]]
    st.bar_chart(chart_data)


def show_line_chart(data, x_col, y_col, title="Trend Chart"):
    """
    Display a line chart
    
    Parameters:
        data: DataFrame
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
    """
    st.markdown(f"### {title}")
    chart_data = data.set_index(x_col)[[y_col]]
    st.line_chart(chart_data)


def show_multi_line_chart(data, x_col, y_cols, title="Multi-Line Chart"):
    """
    Display a multi-line chart
    
    Parameters:
        data: DataFrame
        x_col: Column for x-axis
        y_cols: List of columns for y-axis
        title: Chart title
    """
    st.markdown(f"### {title}")
    chart_data = data.set_index(x_col)[y_cols]
    st.line_chart(chart_data)


def show_area_chart(data, x_col, y_col, title="Area Chart"):
    """
    Display an area chart
    
    Parameters:
        data: DataFrame
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
    """
    st.markdown(f"### {title}")
    chart_data = data.set_index(x_col)[[y_col]]
    st.area_chart(chart_data)