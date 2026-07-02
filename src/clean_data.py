import os
import pandas as pd
import numpy as np
from src.load_data import load_raw_data

# Mapping of unique products to their correct Category and Sub-category
PRODUCT_MAPPING = {
    '4K Monitor': ('Electronics', 'Monitors'),
    'Action Camera': ('Electronics', 'Cameras'),
    'Air Fryer': ('Home & Kitchen', 'Kitchen Appliances'),
    'Backpack': ('Clothing', 'Bags & Accessories'),
    'Bluetooth Speaker': ('Electronics', 'Audio'),
    'Board Game': ('Toys & Games', 'Games'),
    'Car Charger': ('Electronics', 'Mobile Accessories'),
    "Children's Book": ('Books', 'Children'),
    'Cookware Set': ('Home & Kitchen', 'Cookware'),
    'Desk Organizer': ('Home & Kitchen', 'Office Supplies'),
    'Desk Plant': ('Home & Kitchen', 'Home Decor'),
    'Dress Shirt': ('Clothing', 'Apparel'),
    'Drone Mini': ('Electronics', 'Drones'),
    'Electric Kettle': ('Home & Kitchen', 'Kitchen Appliances'),
    'External HDD 2TB': ('Electronics', 'Storage'),
    'Fitness Band': ('Electronics', 'Wearables'),
    'Gaming Mouse': ('Electronics', 'Computer Accessories'),
    'Graphic Tablet': ('Electronics', 'Computer Accessories'),
    'HDMI Cable 2m': ('Electronics', 'Cables & Adapters'),
    'Instant Pot': ('Home & Kitchen', 'Kitchen Appliances'),
    'Jeans': ('Clothing', 'Apparel'),
    'Kids Toy Car': ('Toys & Games', 'Toys'),
    'LED Desk Lamp': ('Home & Kitchen', 'Lighting'),
    'Laptop Sleeve': ('Electronics', 'Bags & Accessories'),
    'Mechanical Keyboard': ('Electronics', 'Computer Accessories'),
    'Memory Card 128GB': ('Electronics', 'Storage'),
    'Microphone': ('Electronics', 'Audio'),
    'Noise Cancelling Headphones': ('Electronics', 'Audio'),
    'Novel Bestseller': ('Books', 'Fiction'),
    'Office Chair': ('Home & Kitchen', 'Furniture'),
    'Phone Tripod': ('Electronics', 'Mobile Accessories'),
    'Portable SSD 1TB': ('Electronics', 'Storage'),
    'Power Bank 20000mAh': ('Electronics', 'Mobile Accessories'),
    'Projector Mini': ('Electronics', 'Visuals'),
    'Puzzle 1000pc': ('Toys & Games', 'Puzzles'),
    'Router': ('Electronics', 'Networking'),
    'Running Shoes': ('Clothing', 'Footwear'),
    'Smart Light Bulb': ('Home & Kitchen', 'Smart Home'),
    'Smartphone Case': ('Electronics', 'Mobile Accessories'),
    'Smartwatch': ('Electronics', 'Wearables'),
    'Sunglasses': ('Clothing', 'Bags & Accessories'),
    'T-Shirt': ('Clothing', 'Apparel'),
    'USB-C Charger': ('Electronics', 'Mobile Accessories'),
    'Vacuum Cleaner': ('Home & Kitchen', 'Home Appliances'),
    'Water Bottle': ('Sports & Outdoors', 'Accessories'),
    'Webcam Full HD': ('Electronics', 'Computer Accessories'),
    'Winter Jacket': ('Clothing', 'Apparel'),
    'Wireless Charger': ('Electronics', 'Mobile Accessories'),
    'Wireless Earbuds': ('Electronics', 'Audio'),
    'Yoga Mat': ('Sports & Outdoors', 'Fitness')
}

# Base Profit Margin per Category
CATEGORY_MARGINS = {
    'Books': 0.40,           # 40% margin
    'Electronics': 0.15,     # 15% margin
    'Home & Kitchen': 0.20,  # 20% margin
    'Toys & Games': 0.30,    # 30% margin
    'Clothing': 0.25,        # 25% margin
    'Sports & Outdoors': 0.25 # 25% margin
}

def clean_sales_data(raw_file_path="data/raw/Amazon_Sales.xlsx", 
                     processed_file_path="data/processed/cleaned_sales.csv"):
    """
    Cleans raw Amazon sales data and outputs the processed CSV.
    """
    # Load
    df = load_raw_data(raw_file_path)
    
    # 1. Handle Missing Values and Duplicates
    print("Checking for null values...")
    print(df.isnull().sum())
    
    df.dropna(subset=['OrderID', 'TotalAmount', 'Quantity', 'UnitPrice'], inplace=True)
    
    duplicates_count = df.duplicated().sum()
    print(f"Removing {duplicates_count} duplicate rows...")
    df.drop_duplicates(inplace=True)
    
    # 2. Date Formatting
    print("Formatting order dates...")
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    
    # 3. Standardize Categorical Values (Category Mismatches)
    print("Correcting product category assignments and extracting sub-categories...")
    
    # Map products using PRODUCT_MAPPING
    df['Category'] = df['ProductName'].apply(lambda x: PRODUCT_MAPPING.get(x, ('Unknown', 'Unknown'))[0])
    df['Sub_Category'] = df['ProductName'].apply(lambda x: PRODUCT_MAPPING.get(x, ('Unknown', 'Unknown'))[1])
    
    # 4. Standardize Location Values
    # Since all states (TX, CA, NY, etc.) are in the US, overwrite Country to 'United States'
    print("Standardizing Country field to 'United States'...")
    df['Country'] = 'United States'
    
    # 5. Outlier Detection and Capping (using IQR)
    print("Detecting and capping price outliers...")
    for col in ['UnitPrice', 'TotalAmount']:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Capping outliers to upper and lower bounds
        df[col] = np.clip(df[col], lower_bound, upper_bound)
    
    # 6. Profit Modeling
    print("Calculating COGS and Profit based on product categories...")
    
    def calculate_cogs_and_profit(row):
        category = row['Category']
        base_margin = CATEGORY_MARGINS.get(category, 0.20)
        
        unit_price = row['UnitPrice']
        quantity = row['Quantity']
        discount = row['Discount']
        tax = row['Tax']
        shipping_cost = row['ShippingCost']
        total_amount = row['TotalAmount']
        
        # Base unit cost price before discount
        unit_cost = unit_price * (1 - base_margin)
        cogs = unit_cost * quantity
        
        # Profit = Total Amount - Cost of Goods Sold - Tax - Shipping Cost
        # Since Total Amount = Quantity * Unit Price * (1 - Discount) + Tax + Shipping Cost,
        # Profit = Quantity * Unit Price * (BaseMargin - Discount)
        profit = quantity * unit_price * (base_margin - discount)
        
        return pd.Series([cogs, profit])
        
    df[['COGS', 'Profit']] = df.apply(calculate_cogs_and_profit, axis=1)
    
    # 7. Add Year and Month columns for ease of analysis
    df['Year'] = df['OrderDate'].dt.year
    df['Month'] = df['OrderDate'].dt.strftime('%m-%B')
    df['MonthYear'] = df['OrderDate'].dt.to_period('M').astype(str)
    
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
    
    # Save cleaned dataset
    print(f"Saving cleaned dataset to: {processed_file_path}...")
    df.to_csv(processed_file_path, index=False)
    print("Data cleaning completed successfully.")
    return df

if __name__ == "__main__":
    clean_sales_data()
