import os
import pandas as pd
from src.clean_data import clean_sales_data
from src.analysis import calculate_kpis, analyze_sales_by_group, preferred_payment_modes, monthly_trends
from src.visualization import (
    generate_sales_by_state_chart,
    generate_category_distribution_chart,
    generate_monthly_trend_chart,
    generate_top_products_chart,
    generate_payment_mode_chart,
    generate_category_profit_chart
)

def main():
    print("=== STARTING AMAZON SALES ANALYTICS PIPELINE ===")
    
    # 1. Clean data and generate processed CSV
    raw_path = "data/raw/Amazon_Sales.xlsx"
    processed_path = "data/processed/cleaned_sales.csv"
    
    df = clean_sales_data(raw_path, processed_path)
    
    # 2. Compute KPIs
    kpi_dict = calculate_kpis(df)
    print("\nPrimary KPIs:")
    for k, v in kpi_dict.items():
        if 'sales' in k or 'profit' in k or 'value' in k:
            print(f"  {k}: ${v:,.2f}")
        elif 'margin' in k:
            print(f"  {k}: {v*100:.2f}%")
        else:
            print(f"  {k}: {v:,}")
            
    # 3. Aggregate Data for Charts
    print("\nAggregating datasets for charts...")
    df_state = analyze_sales_by_group(df, 'State')
    df_cat = analyze_sales_by_group(df, 'Category')
    df_monthly = monthly_trends(df)
    
    # Get top products
    df_prod_grouped = df.groupby('ProductName').agg(TotalSales=('TotalAmount', 'sum')).reset_index()
    
    df_pay = preferred_payment_modes(df)
    
    # 4. Generate Visualizations
    print("\nGenerating charts...")
    generate_sales_by_state_chart(df_state, "images/sales_state.png")
    generate_category_distribution_chart(df_cat, "images/sales_category.png")
    generate_monthly_trend_chart(df_monthly, "images/sales_trend.png")
    generate_top_products_chart(df_prod_grouped, "images/top_products.png")
    generate_payment_mode_chart(df_pay, "images/payment_mode.png")
    generate_category_profit_chart(df_cat, "images/category_profit.png")
    
    print("\n=== PIPELINE RUN COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
