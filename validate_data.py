"""
Data Validation Script
Run this to verify your dataset is correctly loaded
"""

import pandas as pd
import sys

def validate_data():
    """Validate that the CSV file is loaded correctly"""
    
    print("=" * 60)
    print("Superstore Sales Data Validation")
    print("=" * 60)
    print()
    
    # Try to load data
    try:
        # Try UTF-8 encoding first
        try:
            df = pd.read_csv('data/superstore.csv', encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Try latin-1 encoding
                df = pd.read_csv('data/superstore.csv', encoding='latin-1')
            except UnicodeDecodeError:
                try:
                    # Try Windows-1252 encoding
                    df = pd.read_csv('data/superstore.csv', encoding='cp1252')
                except:
                    # Last resort - ignore errors
                    df = pd.read_csv('data/superstore.csv', encoding='utf-8', errors='ignore')
                    
         # Convert date columns to datetime
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
        
        print("✅ superstore.csv loaded successfully!")
        print(f"   - Rows: {len(df):,}")
        print(f"   - Columns: {len(df.columns)}")
        print()
    except FileNotFoundError:
        print("❌ ERROR: data/superstore.csv not found!")
        print("   Please place your Superstore CSV file in the data/ folder")
        print()
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR loading superstore.csv: {e}")
        print()
        sys.exit(1)
    
    # Display column names
    print("📋 Column Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    print()
    
    # Data Statistics
    print("=" * 60)
    print("Data Statistics")
    print("=" * 60)
    print()
    
    print("📊 SALES METRICS:")
    print(f"   - Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"   - Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"   - Total Orders: {df['Order ID'].nunique():,}")
    print(f"   - Total Customers: {df['Customer ID'].nunique():,}")
    print()
    
    print("📦 PRODUCTS:")
    print(f"   - Categories: {df['Category'].nunique()}")
    print(f"   - Sub-Categories: {df['Sub-Category'].nunique()}")
    print(f"   - Unique Products: {df['Product Name'].nunique():,}")
    print()
    
    print("📍 GEOGRAPHIC:")
    print(f"   - Regions: {df['Region'].nunique()}")
    print(f"   - States: {df['State'].nunique()}")
    print(f"   - Cities: {df['City'].nunique()}")
    print()
    
    print("👥 CUSTOMERS:")
    print(f"   - Customer Segments: {df['Segment'].nunique()}")
    print(f"   - Segments: {', '.join(df['Segment'].unique())}")
    print()
    
    # Check for missing values
    print("=" * 60)
    print("Data Quality Check")
    print("=" * 60)
    print()
    
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("⚠️ Missing values found:")
        for col, count in missing[missing > 0].items():
            print(f"   - {col}: {count} missing")
    else:
        print("✅ No missing values found!")
    print()
    
    # Sample data
    print("=" * 60)
    print("Sample Data Preview")
    print("=" * 60)
    print()
    print(df[['Order Date', 'Category', 'Sub-Category', 'Sales', 'Profit']].head(3).to_string(index=False))
    print()
    
    print("=" * 60)
    print("✅ Dataset validation complete! Your data looks good.")
    print("=" * 60)
    print()
    print("You can now run the app with: streamlit run app.py")
    print()

    print("📊 SALES METRICS:")
    print(f"   - Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"   - Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"   - Date Range: {df['Order Date'].min().year} - {df['Order Date'].max().year}")
    print()

    print("📍 GEOGRAPHIC:")
    print(f"   - States: {df['State'].nunique()}")
    print(f"   - Cities: {df['City'].nunique()}")
    print(f"   - Regions: {df['Region'].nunique()}")

if __name__ == "__main__":
    validate_data()