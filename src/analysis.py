import pandas as pd
import numpy as np

def calculate_kpis(df):
    """
    Calculates primary KPIs for the dashboard.
    """
    total_sales = df['TotalAmount'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['OrderID'].nunique()
    avg_sales = df['TotalAmount'].mean()
    avg_profit = df['Profit'].mean()
    max_sales = df['TotalAmount'].max()
    min_sales = df['TotalAmount'].min()
    
    # Average Order Value (AOV) = Total Sales / Total Orders
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    # Profit Margin = Total Profit / Total Sales
    profit_margin = total_profit / total_sales if total_sales > 0 else 0
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_orders': total_orders,
        'avg_sales': avg_sales,
        'avg_profit': avg_profit,
        'max_sales': max_sales,
        'min_sales': min_sales,
        'avg_order_value': avg_order_value,
        'profit_margin': profit_margin
    }

def analyze_sales_by_group(df, group_col):
    """
    Aggregates Sales, Profit, and Order Count by a specified column.
    """
    grouped = df.groupby(group_col).agg(
        TotalSales=('TotalAmount', 'sum'),
        TotalProfit=('Profit', 'sum'),
        TotalQuantity=('Quantity', 'sum'),
        OrderCount=('OrderID', 'nunique')
    ).reset_index()
    
    # Calculate Profit Margin
    grouped['ProfitMargin'] = grouped['TotalProfit'] / grouped['TotalSales']
    return grouped.sort_values(by='TotalSales', ascending=False)

def analyze_multi_level(df, group_cols):
    """
    Performs multi-level aggregation.
    """
    grouped = df.groupby(group_cols).agg(
        TotalSales=('TotalAmount', 'sum'),
        TotalProfit=('Profit', 'sum'),
        TotalQuantity=('Quantity', 'sum')
    ).reset_index()
    return grouped.sort_values(by='TotalSales', ascending=False)

def get_top_bottom_analysis(df, entity_col, value_col='TotalAmount', top_n=10):
    """
    Returns top and bottom N elements by value column.
    """
    grouped = df.groupby(entity_col).agg({value_col: 'sum'}).reset_index()
    top_n_df = grouped.sort_values(by=value_col, ascending=False).head(top_n)
    bottom_n_df = grouped.sort_values(by=value_col, ascending=True).head(top_n)
    return top_n_df, bottom_n_df

def preferred_payment_modes(df):
    """
    Aggregates count and percentage of orders placed by payment method.
    """
    grouped = df.groupby('PaymentMethod').agg(
        OrderCount=('OrderID', 'nunique'),
        TotalSales=('TotalAmount', 'sum')
    ).reset_index()
    grouped['Percentage'] = (grouped['OrderCount'] / grouped['OrderCount'].sum()) * 100
    return grouped.sort_values(by='OrderCount', ascending=False)

def monthly_trends(df):
    """
    Aggregates Sales and Profit by Month-Year.
    """
    grouped = df.groupby(['MonthYear']).agg(
        TotalSales=('TotalAmount', 'sum'),
        TotalProfit=('Profit', 'sum'),
        OrderCount=('OrderID', 'nunique')
    ).reset_index()
    return grouped.sort_values(by='MonthYear')

def correlation_analysis(df):
    """
    Computes Pearson correlation matrix for numeric columns.
    """
    cols = ['Quantity', 'UnitPrice', 'Discount', 'Tax', 'ShippingCost', 'TotalAmount', 'Profit']
    return df[cols].corr()

def customer_segmentation(df):
    """
    Segments customers based on Recency, Frequency, and Monetary (RFM) score principles.
    For simplicity and performance, we'll perform a volume & frequency division:
    - High-Value Loyalists: Orders >= 3 and Total Spent >= $1500
    - Active Spenders: Orders >= 2 and Total Spent < $1500
    - Occasional Buyers: Orders == 1 and Total Spent >= $500
    - New/One-time Buyers: Orders == 1 and Total Spent < $500
    """
    cust_metrics = df.groupby('CustomerID').agg(
        TotalSpent=('TotalAmount', 'sum'),
        OrderCount=('OrderID', 'nunique'),
        CustomerName=('CustomerName', 'first')
    ).reset_index()
    
    def segment_cust(row):
        spent = row['TotalSpent']
        orders = row['OrderCount']
        if orders >= 3 and spent >= 1500:
            return 'High-Value Loyalist'
        elif orders >= 2:
            return 'Active Spender'
        elif spent >= 500:
            return 'Occasional Buyer'
        else:
            return 'One-time Buyer'
            
    cust_metrics['Segment'] = cust_metrics.apply(segment_cust, axis=1)
    return cust_metrics

def pareto_analysis(df, entity_col='ProductName'):
    """
    Performs 80-20 Pareto analysis on Sales.
    """
    grouped = df.groupby(entity_col).agg(TotalSales=('TotalAmount', 'sum')).reset_index()
    grouped = grouped.sort_values(by='TotalSales', ascending=False)
    grouped['CumulativeSales'] = grouped['TotalSales'].cumsum()
    total_sales = grouped['TotalSales'].sum()
    grouped['CumulativePercentage'] = (grouped['CumulativeSales'] / total_sales) * 100
    return grouped
