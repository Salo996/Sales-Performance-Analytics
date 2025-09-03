#!/usr/bin/env python3
"""
Sales Performance Analytics - Data Extraction Script
===================================================

This script extracts data from the DummyJSON API and prepares it for analysis.
Created by: Salomón Santiago Esquivel
Project: Sales Performance Analytics Dashboard

Data Sources:
- Products: https://dummyjson.com/products
- Users: https://dummyjson.com/users  
- Carts: https://dummyjson.com/carts

Usage:
    python data_extraction.py
    
Output:
    - products.csv
    - users.csv
    - carts.csv
    - sales_data.db (SQLite database)
"""

import requests
import pandas as pd
import sqlite3
import json
from datetime import datetime
import os

class SalesDataExtractor:
    """Extract and process sales data from DummyJSON API"""
    
    def __init__(self, base_url="https://dummyjson.com"):
        self.base_url = base_url
        self.data_dir = "../data"
        self.db_path = "../data/sales_data.db"
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
    def fetch_data(self, endpoint):
        """Fetch data from API endpoint with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            print(f"Fetching data from: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"Successfully fetched {endpoint} data")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return None
    
    def extract_products(self):
        """Extract and process products data"""
        print("\nExtracting Products Data...")
        
        # Get all products (DummyJSON returns 30 products by default)
        data = self.fetch_data("products")
        
        if data and 'products' in data:
            products = data['products']
            
            # Create DataFrame
            df = pd.DataFrame(products)
            
            # Select relevant columns for analysis
            columns_to_keep = [
                'id', 'title', 'description', 'price', 'discountPercentage', 
                'rating', 'stock', 'brand', 'category', 'thumbnail'
            ]
            
            df = df[columns_to_keep].copy()
            
            # Data cleaning and transformation
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            df['stock'] = pd.to_numeric(df['stock'], errors='coerce')
            df['discountPercentage'] = pd.to_numeric(df['discountPercentage'], errors='coerce')
            
            # Add calculated columns
            df['revenue_potential'] = df['price'] * df['stock']
            df['discounted_price'] = df['price'] * (1 - df['discountPercentage'] / 100)
            df['extraction_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Save to CSV
            csv_path = f"{self.data_dir}/products.csv"
            df.to_csv(csv_path, index=False)
            print(f"Products data saved to: {csv_path}")
            print(f"Total products: {len(df)}")
            print(f"Categories: {df['category'].nunique()}")
            
            return df
        
        return None
    
    def extract_users(self):
        """Extract and process users data"""
        print("\nExtracting Users Data...")
        
        data = self.fetch_data("users")
        
        if data and 'users' in data:
            users = data['users']
            
            # Create DataFrame
            df = pd.DataFrame(users)
            
            # Select relevant columns
            columns_to_keep = [
                'id', 'firstName', 'lastName', 'age', 'gender', 'email',
                'phone', 'birthDate', 'address'
            ]
            
            df_clean = df[columns_to_keep].copy()
            
            # Extract address information
            if 'address' in df_clean.columns:
                # Normalize address data (it comes as nested dict)
                address_df = pd.json_normalize(df_clean['address'])
                df_clean = pd.concat([df_clean.drop('address', axis=1), address_df], axis=1)
            
            # Data cleaning
            df_clean['age'] = pd.to_numeric(df_clean['age'], errors='coerce')
            df_clean['extraction_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Add age groups for segmentation
            df_clean['age_group'] = df_clean['age'].apply(self.categorize_age)
            
            # Save to CSV
            csv_path = f"{self.data_dir}/users.csv"
            df_clean.to_csv(csv_path, index=False)
            print(f"Users data saved to: {csv_path}")
            print(f"Total users: {len(df_clean)}")
            print(f"Age range: {df_clean['age'].min()}-{df_clean['age'].max()}")
            
            return df_clean
        
        return None
    
    def extract_carts(self):
        """Extract and process carts data"""
        print("\nExtracting Carts Data...")
        
        data = self.fetch_data("carts")
        
        if data and 'carts' in data:
            carts = data['carts']
            
            # Create main carts DataFrame
            carts_df = pd.DataFrame(carts)
            
            # Select main cart columns
            cart_columns = ['id', 'userId', 'total', 'discountedTotal', 'totalProducts', 'totalQuantity']
            carts_clean = carts_df[cart_columns].copy()
            
            # Data cleaning
            for col in ['total', 'discountedTotal', 'totalProducts', 'totalQuantity']:
                carts_clean[col] = pd.to_numeric(carts_clean[col], errors='coerce')
            
            carts_clean['extraction_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Calculate savings
            carts_clean['total_savings'] = carts_clean['total'] - carts_clean['discountedTotal']
            carts_clean['savings_percentage'] = (carts_clean['total_savings'] / carts_clean['total'] * 100).round(2)
            
            # Save to CSV
            csv_path = f"{self.data_dir}/carts.csv"
            carts_clean.to_csv(csv_path, index=False)
            print(f"Carts data saved to: {csv_path}")
            print(f"Total carts: {len(carts_clean)}")
            print(f"Total sales volume: ${carts_clean['total'].sum():,.2f}")
            
            # Also extract cart items for detailed analysis
            cart_items = []
            for cart in carts:
                cart_id = cart['id']
                user_id = cart['userId']
                for product in cart['products']:
                    item = {
                        'cart_id': cart_id,
                        'user_id': user_id,
                        'product_id': product['id'],
                        'product_title': product['title'],
                        'price': product['price'],
                        'quantity': product['quantity'],
                        'total': product['total'],
                        'discount_percentage': product.get('discountPercentage', 0),
                        'discounted_price': product.get('discountedPrice', product['price'])
                    }
                    cart_items.append(item)
            
            # Save cart items
            if cart_items:
                items_df = pd.DataFrame(cart_items)
                items_csv_path = f"{self.data_dir}/cart_items.csv"
                items_df.to_csv(items_csv_path, index=False)
                print(f"Cart items saved to: {items_csv_path}")
                print(f"Total items: {len(items_df)}")
            
            return carts_clean, pd.DataFrame(cart_items) if cart_items else None
        
        return None, None
    
    def categorize_age(self, age):
        """Categorize age into meaningful groups"""
        if pd.isna(age):
            return 'Unknown'
        elif age < 25:
            return 'Gen Z (Under 25)'
        elif 25 <= age <= 35:
            return 'Millennials (25-35)'
        elif 36 <= age <= 50:
            return 'Gen X (36-50)'
        else:
            return 'Boomers (50+)'
    
    def create_sqlite_database(self, products_df, users_df, carts_df, cart_items_df):
        """Create SQLite database with all tables"""
        print("\nCreating SQLite Database...")
        
        try:
            # Connect to SQLite database
            conn = sqlite3.connect(self.db_path)
            
            # Save DataFrames to database tables
            if products_df is not None:
                products_df.to_sql('products', conn, if_exists='replace', index=False)
                print("Products table created")
            
            if users_df is not None:
                users_df.to_sql('users', conn, if_exists='replace', index=False)
                print("Users table created")
            
            if carts_df is not None:
                carts_df.to_sql('carts', conn, if_exists='replace', index=False)
                print("Carts table created")
            
            if cart_items_df is not None:
                cart_items_df.to_sql('cart_items', conn, if_exists='replace', index=False)
                print("Cart_items table created")
            
            # Create indexes for better query performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_age ON users(age)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_carts_userId ON carts(userId)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cart_items_product_id ON cart_items(product_id)")
            
            conn.close()
            print(f"Database successfully created at: {self.db_path}")
            
        except Exception as e:
            print(f"Error creating database: {e}")
    
    def run_extraction(self):
        """Run the complete data extraction process"""
        print("Starting Sales Performance Data Extraction")
        print("=" * 60)
        
        # Extract all data
        products_df = self.extract_products()
        users_df = self.extract_users()
        carts_df, cart_items_df = self.extract_carts()
        
        # Create database
        self.create_sqlite_database(products_df, users_df, carts_df, cart_items_df)
        
        print("\n" + "=" * 60)
        print("Data extraction completed successfully!")
        print("\nFiles created:")
        print(f"   - {self.data_dir}/products.csv")
        print(f"   - {self.data_dir}/users.csv") 
        print(f"   - {self.data_dir}/carts.csv")
        print(f"   - {self.data_dir}/cart_items.csv")
        print(f"   - {self.db_path}")
        
        # Summary statistics
        if products_df is not None:
            print(f"\nData Summary:")
            print(f"   - Products: {len(products_df)} items")
            print(f"   - Categories: {products_df['category'].nunique()}")
            print(f"   - Price range: ${products_df['price'].min():.2f} - ${products_df['price'].max():.2f}")
        
        if users_df is not None:
            print(f"   - Users: {len(users_df)} customers")
            print(f"   - Age range: {users_df['age'].min()}-{users_df['age'].max()} years")
        
        if carts_df is not None:
            print(f"   - Carts: {len(carts_df)} transactions")
            print(f"   - Total sales: ${carts_df['total'].sum():,.2f}")
        
        print(f"\nReady for SQL analysis!")

def main():
    """Main execution function"""
    extractor = SalesDataExtractor()
    extractor.run_extraction()

if __name__ == "__main__":
    main()