import os
import matplotlib.pyplot as plt
import numpy as np

# Apply professional style settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['grid.linestyle'] = '--'

# Premium Color Palette
TEAL = '#008080'
AMBER = '#FFBF00'
DARK_GREY = '#2F4F4F'
SLATE = '#708090'
CORAL = '#FF7F50'
DEEP_BLUE = '#1F4E79'
LIGHT_BLUE = '#8FAADC'
LIGHT_GREEN = '#A9D08E'

COLORS = [DEEP_BLUE, TEAL, CORAL, AMBER, SLATE, LIGHT_GREEN]

def generate_sales_by_state_chart(df_state, save_path="images/sales_state.png"):
    """
    Creates a bar chart showing Sales by State.
    """
    plt.figure(figsize=(10, 6))
    df_sorted = df_state.sort_values(by='TotalSales', ascending=True)
    
    # Horizontal bar chart for better state label layout
    bars = plt.barh(df_sorted['State'], df_sorted['TotalSales'] / 1e6, color=DEEP_BLUE, height=0.6)
    
    # Add values on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f"M${width:.2f}", 
                 va='center', ha='left', fontsize=9, color='#333333', fontweight='semibold')
                 
    plt.title("Total Sales by U.S. State", fontweight='bold', pad=15)
    plt.xlabel("Sales (in Millions USD)", fontweight='semibold', labelpad=10)
    plt.ylabel("State", fontweight='semibold', labelpad=10)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def generate_category_distribution_chart(df_cat, save_path="images/sales_category.png"):
    """
    Creates a Pie/Donut Chart showing Category-wise Sales.
    """
    plt.figure(figsize=(8, 7))
    
    # Sales breakdown
    labels = df_cat['Category']
    sales = df_cat['TotalSales']
    
    # Donut Chart
    wedges, texts, autotexts = plt.pie(
        sales, labels=labels, autopct='%1.1f%%', startangle=140, 
        colors=COLORS, pctdistance=0.75, 
        textprops=dict(color="black", fontsize=10, fontweight='semibold'),
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    
    plt.title("Sales Distribution by Product Category", fontweight='bold', pad=15)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def generate_monthly_trend_chart(df_monthly, save_path="images/sales_trend.png"):
    """
    Creates a Line Chart showing Monthly Sales and Profit Trend.
    """
    plt.figure(figsize=(12, 6))
    
    df_sorted = df_monthly.sort_values(by='MonthYear')
    months = df_sorted['MonthYear']
    sales_m = df_sorted['TotalSales'] / 1e6
    profit_m = df_sorted['TotalProfit'] / 1e6
    
    plt.plot(months, sales_m, marker='o', linewidth=2.5, color=DEEP_BLUE, label='Total Sales (M$)')
    plt.plot(months, profit_m, marker='s', linewidth=2, color=CORAL, linestyle='--', label='Total Profit (M$)')
    
    # Customize labels and rotation
    plt.xticks(rotation=45, ha='right')
    plt.title("Monthly Sales and Profit Trend (2020 - 2024)", fontweight='bold', pad=15)
    plt.xlabel("Month", fontweight='semibold', labelpad=10)
    plt.ylabel("Amount (in Millions USD)", fontweight='semibold', labelpad=10)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def generate_top_products_chart(df_prod, save_path="images/top_products.png"):
    """
    Creates a horizontal bar chart showing Top 10 Products by Sales.
    """
    plt.figure(figsize=(10, 6))
    df_sorted = df_prod.sort_values(by='TotalSales', ascending=True).tail(10)
    
    bars = plt.barh(df_sorted['ProductName'], df_sorted['TotalSales'] / 1e3, color=TEAL, height=0.6)
    
    # Add values on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 2, bar.get_y() + bar.get_height()/2, f"${width:,.1f}K", 
                 va='center', ha='left', fontsize=9, color='#333333', fontweight='semibold')
                 
    plt.title("Top 10 Products by Total Sales", fontweight='bold', pad=15)
    plt.xlabel("Sales (in Thousands USD)", fontweight='semibold', labelpad=10)
    plt.ylabel("Product Name", fontweight='semibold', labelpad=10)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def generate_payment_mode_chart(df_pay, save_path="images/payment_mode.png"):
    """
    Creates a pie chart showing payment mode preference distribution.
    """
    plt.figure(figsize=(8, 7))
    
    labels = df_pay['PaymentMethod']
    counts = df_pay['OrderCount']
    
    wedges, texts, autotexts = plt.pie(
        counts, labels=labels, autopct='%1.1f%%', startangle=90, 
        colors=COLORS, pctdistance=0.8,
        textprops=dict(color="black", fontsize=10, fontweight='semibold'),
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    
    plt.title("Order Distribution by Payment Mode", fontweight='bold', pad=15)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def generate_category_profit_chart(df_cat, save_path="images/category_profit.png"):
    """
    Creates a column chart comparing Sales vs Profit by Category.
    """
    plt.figure(figsize=(10, 6))
    
    categories = df_cat['Category']
    sales_m = df_cat['TotalSales'] / 1e6
    profit_m = df_cat['TotalProfit'] / 1e6
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, sales_m, width, label='Sales (M$)', color=DEEP_BLUE)
    rects2 = ax.bar(x + width/2, profit_m, width, label='Profit (M$)', color=AMBER)
    
    ax.set_ylabel('Amount (in Millions USD)', fontweight='semibold')
    ax.set_title('Sales vs Profit by Product Category', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    # Label bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}M',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
                        
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")
