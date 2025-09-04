#!/usr/bin/env python3
"""
Sales Performance Analytics - Visualization Dashboard
====================================================

This script creates professional charts and dashboards from the sales data
for portfolio presentation and business intelligence reporting.

Created by: Salomón Santiago Esquivel
Project: Sales Performance Analytics Dashboard

Usage:
    python create_visualizations.py
    
Output:
    - Professional charts saved to visualizations/ folder
    - Dashboard images for portfolio presentation
    - Interactive plots for business presentations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime
import numpy as np
import os

# Set style for professional charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SalesVisualizationDashboard:
    """Create professional visualizations for Sales Performance Analytics"""
    
    def __init__(self):
        self.db_path = "../data/sales_data.db"
        self.output_dir = "../visualizations"
        
        # Create visualizations directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Professional color scheme
        self.colors = {
            'primary': '#2E86C1',      # Professional blue
            'secondary': '#28B463',     # Success green  
            'accent': '#F39C12',        # Warning orange
            'danger': '#E74C3C',        # Alert red
            'dark': '#2C3E50',          # Dark blue-gray
            'light': '#ECF0F1'          # Light gray
        }
        
        # Load data
        self.load_data()
        
    def load_data(self):
        """Load data from SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            
            # Load main datasets
            self.products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
            self.users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
            self.carts_df = pd.read_sql_query("SELECT * FROM carts", self.conn)
            self.cart_items_df = pd.read_sql_query("SELECT * FROM cart_items", self.conn)
            
            print(f"Data loaded successfully:")
            print(f"   - Products: {len(self.products_df)} items")
            print(f"   - Users: {len(self.users_df)} customers")  
            print(f"   - Carts: {len(self.carts_df)} transactions")
            print(f"   - Cart Items: {len(self.cart_items_df)} line items")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def create_revenue_by_category_chart(self):
        """Chart 1: Revenue Analysis by Category"""
        print("\nCreating Revenue by Category Chart...")
        
        # Calculate revenue potential by category
        revenue_data = self.products_df.groupby('category').agg({
            'price': ['count', 'mean'],
            'stock': 'sum',
            'rating': 'mean'
        }).round(2)
        
        # Calculate revenue potential
        revenue_data['revenue_potential'] = (self.products_df.groupby('category')
                                           .apply(lambda x: (x['price'] * x['stock']).sum()))
        
        # Flatten column names
        revenue_data.columns = ['product_count', 'avg_price', 'total_stock', 'avg_rating', 'revenue_potential']
        revenue_data = revenue_data.sort_values('revenue_potential', ascending=False)
        
        # Create the visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Sales Performance Analytics: Revenue Analysis by Category', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # Chart 1: Revenue Potential by Category (Bar Chart)
        categories = revenue_data.index
        revenues = revenue_data['revenue_potential']
        
        bars1 = ax1.bar(categories, revenues, color=self.colors['primary'], alpha=0.8, edgecolor='white', linewidth=2)
        ax1.set_title('Revenue Potential by Category', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Revenue Potential ($)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars1, revenues):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenues)*0.01,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Chart 2: Average Rating by Category (Horizontal Bar)
        ratings = revenue_data['avg_rating']
        bars2 = ax2.barh(categories, ratings, color=self.colors['secondary'], alpha=0.8, edgecolor='white', linewidth=2)
        ax2.set_title('Average Rating by Category', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Average Rating', fontsize=12)
        ax2.set_xlim(0, 5)
        
        # Add value labels
        for bar, value in zip(bars2, ratings):
            ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                    f'{value:.2f}', ha='left', va='center', fontweight='bold', fontsize=10)
        
        # Chart 3: Product Count vs Average Price (Scatter)
        ax3.scatter(revenue_data['product_count'], revenue_data['avg_price'], 
                   s=200, alpha=0.8, color=self.colors['accent'], edgecolors='white', linewidth=2)
        
        # Add category labels
        for i, category in enumerate(categories):
            ax3.annotate(category, (revenue_data['product_count'].iloc[i], revenue_data['avg_price'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontweight='bold', fontsize=10)
                        
        ax3.set_title('Product Count vs Average Price', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Number of Products', fontsize=12)
        ax3.set_ylabel('Average Price ($)', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # Chart 4: Stock Distribution (Pie Chart)
        stock_data = revenue_data['total_stock']
        wedges, texts, autotexts = ax4.pie(stock_data, labels=categories, autopct='%1.1f%%',
                                          colors=[self.colors['primary'], self.colors['secondary'], 
                                                 self.colors['accent'], self.colors['danger']], 
                                          startangle=90, explode=[0.05]*len(categories))
        
        ax4.set_title('Stock Distribution by Category', fontsize=14, fontweight='bold')
        
        # Enhance pie chart text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        plt.tight_layout()
        
        # Save chart
        chart_path = f"{self.output_dir}/01_revenue_by_category_dashboard.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"Chart saved: {chart_path}")
        return revenue_data
        
    def create_customer_segmentation_chart(self):
        """Chart 2: Customer Segmentation Analysis"""
        print("\nCreating Customer Segmentation Chart...")
        
        # Create age segments
        def categorize_age(age):
            if age < 25:
                return 'Gen Z (Under 25)'
            elif 25 <= age <= 35:
                return 'Millennials (25-35)'
            elif 36 <= age <= 50:
                return 'Gen X (36-50)'
            else:
                return 'Boomers (50+)'
        
        self.users_df['age_segment'] = self.users_df['age'].apply(categorize_age)
        
        # Analyze customer segments
        segment_data = self.users_df.groupby('age_segment').agg({
            'age': ['count', 'mean', 'min', 'max'],
            'gender': lambda x: x.value_counts().to_dict()
        })
        
        # Flatten and clean the data
        segment_summary = self.users_df.groupby('age_segment').agg({
            'age': ['count', 'mean']
        }).round(1)
        segment_summary.columns = ['customer_count', 'avg_age']
        segment_summary['percentage'] = (segment_summary['customer_count'] / 
                                       segment_summary['customer_count'].sum() * 100).round(1)
        
        # Create visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Sales Performance Analytics: Customer Segmentation Analysis', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # Chart 1: Customer Count by Age Segment (Bar Chart)
        segments = segment_summary.index
        counts = segment_summary['customer_count']
        
        bars1 = ax1.bar(segments, counts, color=self.colors['secondary'], alpha=0.8, edgecolor='white', linewidth=2)
        ax1.set_title('Customer Count by Age Segment', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Customers', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add percentage labels
        for bar, count, pct in zip(bars1, counts, segment_summary['percentage']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.02,
                    f'{count}\n({pct}%)', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Chart 2: Age Distribution (Box Plot)
        age_by_segment = [self.users_df[self.users_df['age_segment'] == seg]['age'].values 
                         for seg in segments]
        
        bp = ax2.boxplot(age_by_segment, labels=segments, patch_artist=True)
        ax2.set_title('Age Distribution by Segment', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Age', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # Color the box plots
        colors_list = [self.colors['primary'], self.colors['accent'], self.colors['secondary'], self.colors['danger']]
        for patch, color in zip(bp['boxes'], colors_list[:len(segments)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Chart 3: Gender Distribution by Age Segment (Stacked Bar)
        gender_pivot = self.users_df.groupby(['age_segment', 'gender']).size().unstack(fill_value=0)
        
        gender_pivot.plot(kind='bar', stacked=True, ax=ax3, 
                         color=[self.colors['primary'], self.colors['accent']], alpha=0.8)
        ax3.set_title('Gender Distribution by Age Segment', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Number of Customers', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        ax3.legend(title='Gender', fontsize=10)
        
        # Chart 4: Customer Segment Pie Chart
        wedges, texts, autotexts = ax4.pie(segment_summary['customer_count'], 
                                          labels=segments, autopct='%1.1f%%',
                                          colors=colors_list[:len(segments)], 
                                          startangle=90, explode=[0.05]*len(segments))
        
        ax4.set_title('Customer Segment Distribution', fontsize=14, fontweight='bold')
        
        # Enhance pie chart
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        plt.tight_layout()
        
        # Save chart
        chart_path = f"{self.output_dir}/02_customer_segmentation_dashboard.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"Chart saved: {chart_path}")
        return segment_summary
        
    def create_sales_performance_chart(self):
        """Chart 3: Sales Performance and Customer Value Analysis"""
        print("\nCreating Sales Performance Chart...")
        
        # Merge cart data with user data for customer analysis
        customer_sales = self.carts_df.merge(self.users_df[['id', 'age', 'gender']], 
                                           left_on='userId', right_on='id', how='left')
        
        # Customer value segmentation
        customer_metrics = self.carts_df.groupby('userId').agg({
            'total': ['sum', 'mean', 'count'],
            'totalQuantity': 'sum'
        }).round(2)
        customer_metrics.columns = ['total_spent', 'avg_order_value', 'order_count', 'total_items']
        
        # Add customer segments
        def customer_value_segment(row):
            if row['total_spent'] >= 1500 and row['order_count'] >= 3:
                return 'Premium Customer'
            elif row['total_spent'] >= 800 and row['order_count'] >= 2:
                return 'Valuable Customer'
            elif row['total_spent'] >= 400 or row['order_count'] >= 2:
                return 'Regular Customer'
            else:
                return 'Low-Value Customer'
        
        customer_metrics['customer_segment'] = customer_metrics.apply(customer_value_segment, axis=1)
        
        # Create visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Sales Performance Analytics: Customer Value & Sales Analysis', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # Chart 1: Customer Value Segments (Bar Chart)
        segment_counts = customer_metrics['customer_segment'].value_counts()
        
        bars1 = ax1.bar(segment_counts.index, segment_counts.values, 
                       color=self.colors['primary'], alpha=0.8, edgecolor='white', linewidth=2)
        ax1.set_title('Customer Value Segmentation', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Customers', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, value in zip(bars1, segment_counts.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(segment_counts.values)*0.02,
                    f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Chart 2: Sales Distribution (Histogram)
        ax2.hist(customer_metrics['total_spent'], bins=15, alpha=0.8, 
                color=self.colors['secondary'], edgecolor='white', linewidth=1)
        ax2.set_title('Customer Spending Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Total Spent ($)', fontsize=12)
        ax2.set_ylabel('Number of Customers', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: Order Value vs Order Count (Scatter)
        colors_map = {'Premium Customer': self.colors['danger'], 'Valuable Customer': self.colors['secondary'],
                     'Regular Customer': self.colors['accent'], 'Low-Value Customer': self.colors['primary']}
        
        for segment in customer_metrics['customer_segment'].unique():
            segment_data = customer_metrics[customer_metrics['customer_segment'] == segment]
            ax3.scatter(segment_data['order_count'], segment_data['avg_order_value'],
                       label=segment, alpha=0.8, s=80, color=colors_map[segment], edgecolor='white')
        
        ax3.set_title('Average Order Value vs Order Frequency', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Number of Orders', fontsize=12)
        ax3.set_ylabel('Average Order Value ($)', fontsize=12)
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)
        
        # Chart 4: Top Customers (Horizontal Bar)
        top_customers = customer_metrics.nlargest(10, 'total_spent')['total_spent']
        
        bars4 = ax4.barh(range(len(top_customers)), top_customers.values, 
                        color=self.colors['accent'], alpha=0.8, edgecolor='white', linewidth=2)
        ax4.set_title('Top 10 Customers by Total Spending', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Total Spent ($)', fontsize=12)
        ax4.set_yticks(range(len(top_customers)))
        ax4.set_yticklabels([f'Customer {i+1}' for i in range(len(top_customers))])
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars4, top_customers.values)):
            ax4.text(bar.get_width() + max(top_customers.values)*0.01, bar.get_y() + bar.get_height()/2,
                    f'${value:,.0f}', ha='left', va='center', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        
        # Save chart
        chart_path = f"{self.output_dir}/03_sales_performance_dashboard.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"Chart saved: {chart_path}")
        return customer_metrics
        
    def create_executive_summary_dashboard(self):
        """Chart 4: Executive Summary Dashboard"""
        print("\nCreating Executive Summary Dashboard...")
        
        # Calculate key metrics
        total_revenue = self.carts_df['total'].sum()
        total_customers = len(self.users_df)
        total_orders = len(self.carts_df)
        avg_order_value = self.carts_df['total'].mean()
        total_products = len(self.products_df)
        total_categories = self.products_df['category'].nunique()
        
        # Revenue by category
        revenue_by_category = self.products_df.groupby('category').apply(
            lambda x: (x['price'] * x['stock']).sum()
        ).sort_values(ascending=False)
        
        # Customer age distribution
        avg_customer_age = self.users_df['age'].mean()
        
        # Top performing products
        top_products = self.products_df.nlargest(5, 'rating')[['title', 'rating', 'price', 'category']]
        
        # Create dashboard
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('Sales Performance Analytics: Executive Dashboard Summary', 
                     fontsize=24, fontweight='bold', y=0.95)
        
        # Create grid layout
        gs = fig.add_gridspec(3, 4, height_ratios=[1, 2, 2], width_ratios=[1, 1, 1, 1])
        
        # KPI Cards (Top Row)
        kpi_data = [
            ('Total Revenue', f'${total_revenue:,.0f}', self.colors['primary']),
            ('Total Customers', f'{total_customers:,}', self.colors['secondary']),
            ('Total Orders', f'{total_orders:,}', self.colors['accent']),
            ('Avg Order Value', f'${avg_order_value:.0f}', self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(kpi_data):
            ax = fig.add_subplot(gs[0, i])
            ax.text(0.5, 0.7, value, ha='center', va='center', fontsize=20, fontweight='bold', color=color)
            ax.text(0.5, 0.3, title, ha='center', va='center', fontsize=12, fontweight='bold')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            # Add colored border
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color(color)
                spine.set_linewidth(3)
        
        # Revenue by Category (Middle Left)
        ax1 = fig.add_subplot(gs[1, :2])
        bars = ax1.bar(revenue_by_category.index, revenue_by_category.values, 
                      color=[self.colors['primary'], self.colors['secondary'], 
                            self.colors['accent'], self.colors['danger']], 
                      alpha=0.8, edgecolor='white', linewidth=2)
        ax1.set_title('Revenue Potential by Category', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Revenue Potential ($)', fontsize=12)
        
        # Add value labels
        for bar, value in zip(bars, revenue_by_category.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue_by_category.values)*0.02,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Customer Age Distribution (Middle Right)
        ax2 = fig.add_subplot(gs[1, 2:])
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['Gen Z (<25)', 'Millennials (25-35)', 'Gen X (35-50)', 'Boomers (50+)'])
        ).size()
        
        wedges, texts, autotexts = ax2.pie(age_segments.values, labels=age_segments.index, autopct='%1.1f%%',
                                          colors=[self.colors['primary'], self.colors['secondary'], 
                                                 self.colors['accent'], self.colors['danger']], 
                                          startangle=90, explode=[0.05]*len(age_segments))
        ax2.set_title('Customer Age Distribution', fontsize=16, fontweight='bold')
        
        # Enhance pie chart
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # Top Products Table (Bottom Left)
        ax3 = fig.add_subplot(gs[2, :2])
        ax3.axis('tight')
        ax3.axis('off')
        
        table_data = []
        for _, product in top_products.iterrows():
            table_data.append([product['title'][:20] + '...' if len(product['title']) > 20 else product['title'],
                              f"{product['rating']:.2f}",
                              f"${product['price']:.0f}",
                              product['category'].title()])
        
        table = ax3.table(cellText=table_data,
                         colLabels=['Product Name', 'Rating', 'Price', 'Category'],
                         cellLoc='center',
                         loc='center',
                         colWidths=[0.4, 0.15, 0.15, 0.3])
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 2)
        
        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(4):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor(self.colors['primary'])
                    table[(i, j)].set_text_props(weight='bold', color='white')
                else:
                    table[(i, j)].set_facecolor('#F8F9FA' if i % 2 == 0 else 'white')
        
        ax3.set_title('Top 5 Products by Rating', fontsize=16, fontweight='bold', y=1.1)
        
        # Business Insights (Bottom Right)
        ax4 = fig.add_subplot(gs[2, 2:])
        ax4.axis('off')
        
        insights = [
            "KEY INSIGHTS:",
            "",
            f"- {revenue_by_category.index[0].title()} category leads revenue potential",
            f"- Average customer age: {avg_customer_age:.0f} years",
            f"- {len(self.carts_df[self.carts_df.groupby('userId')['userId'].transform('count') > 1])} repeat customers",
            f"- Top product rating: {top_products.iloc[0]['rating']:.2f}/5.0",
            "",
            "RECOMMENDATIONS:",
            "",
            "- Focus marketing on top category",
            "- Develop retention programs",
            "- Optimize high-rated products",
            "- Target primary age segment"
        ]
        
        for i, insight in enumerate(insights):
            weight = 'bold' if insight.startswith(('KEY', 'RECOMMENDATIONS')) else 'normal'
            size = 12 if insight.startswith(('KEY', 'RECOMMENDATIONS')) else 10
            ax4.text(0.05, 0.95 - i*0.07, insight, fontsize=size, fontweight=weight, 
                    transform=ax4.transAxes, va='top')
        
        plt.tight_layout()
        
        # Save dashboard
        chart_path = f"{self.output_dir}/04_executive_summary_dashboard.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"Executive Dashboard saved: {chart_path}")
        
        # Return summary data
        return {
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'total_orders': total_orders,
            'avg_order_value': avg_order_value,
            'top_category': revenue_by_category.index[0],
            'avg_age': avg_customer_age
        }
        
    def create_portfolio_showcase_image(self):
        """Create main portfolio showcase image"""
        print("\nCreating Portfolio Showcase Image...")
        
        # Create a comprehensive showcase image
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Sales Performance Analytics Dashboard\nSalomón Santiago Esquivel - Data Analyst Portfolio', 
                     fontsize=24, fontweight='bold', y=0.95)
        
        # Chart 1: Revenue by Category
        revenue_data = self.products_df.groupby('category').apply(lambda x: (x['price'] * x['stock']).sum())
        bars1 = ax1.bar(revenue_data.index, revenue_data.values, 
                       color=[self.colors['primary'], self.colors['secondary'], self.colors['accent'], self.colors['danger']], 
                       alpha=0.9, edgecolor='white', linewidth=3)
        ax1.set_title('Revenue Potential by Category', fontsize=18, fontweight='bold', pad=20)
        ax1.set_ylabel('Revenue Potential ($)', fontsize=14)
        
        # Add value labels
        for bar, value in zip(bars1, revenue_data.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue_data.values)*0.02,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Chart 2: Customer Segmentation
        age_segments = self.users_df.groupby(
            pd.cut(self.users_df['age'], bins=[0, 25, 35, 50, 100], 
                   labels=['Gen Z\n(<25)', 'Millennials\n(25-35)', 'Gen X\n(35-50)', 'Boomers\n(50+)'])
        ).size()
        
        wedges, texts, autotexts = ax2.pie(age_segments.values, labels=age_segments.index, autopct='%1.1f%%',
                                          colors=[self.colors['primary'], self.colors['secondary'], 
                                                 self.colors['accent'], self.colors['danger']], 
                                          startangle=90, explode=[0.1]*len(age_segments))
        ax2.set_title('Customer Age Segmentation', fontsize=18, fontweight='bold', pad=20)
        
        # Enhance pie chart
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        # Chart 3: Sales Performance
        customer_sales = self.carts_df.groupby('userId')['total'].sum().sort_values(ascending=False)[:15]
        bars3 = ax3.bar(range(len(customer_sales)), customer_sales.values, 
                       color=self.colors['secondary'], alpha=0.9, edgecolor='white', linewidth=2)
        ax3.set_title('Top 15 Customers by Total Spending', fontsize=18, fontweight='bold', pad=20)
        ax3.set_ylabel('Total Spent ($)', fontsize=14)
        ax3.set_xlabel('Customer Rank', fontsize=14)
        
        # Chart 4: Product Ratings
        rating_dist = self.products_df.groupby('category')['rating'].mean()
        bars4 = ax4.bar(rating_dist.index, rating_dist.values, 
                       color=[self.colors['accent'], self.colors['primary'], self.colors['secondary'], self.colors['danger']], 
                       alpha=0.9, edgecolor='white', linewidth=3)
        ax4.set_title('Average Product Rating by Category', fontsize=18, fontweight='bold', pad=20)
        ax4.set_ylabel('Average Rating', fontsize=14)
        ax4.set_ylim(0, 5)
        
        # Add value labels
        for bar, value in zip(bars4, rating_dist.values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        
        # Save portfolio showcase
        showcase_path = f"{self.output_dir}/sales_performance_analytics_portfolio_showcase.png"
        plt.savefig(showcase_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"Portfolio Showcase saved: {showcase_path}")
        return showcase_path
        
    def generate_all_visualizations(self):
        """Generate all visualizations for the project"""
        print("Starting Sales Performance Analytics Visualization Generation")
        print("=" * 80)
        
        try:
            # Generate all charts
            revenue_data = self.create_revenue_by_category_chart()
            segment_data = self.create_customer_segmentation_chart()
            sales_data = self.create_sales_performance_chart()
            summary_data = self.create_executive_summary_dashboard()
            showcase_path = self.create_portfolio_showcase_image()
            
            print("\n" + "=" * 80)
            print("All visualizations created successfully!")
            print(f"\nOutput directory: {self.output_dir}")
            print(f"Charts created:")
            print(f"   1. Revenue by Category Dashboard")
            print(f"   2. Customer Segmentation Dashboard") 
            print(f"   3. Sales Performance Dashboard")
            print(f"   4. Executive Summary Dashboard")
            print(f"   5. Portfolio Showcase Image")
            
            print(f"\nKey Business Insights:")
            print(f"   - Total Revenue Analyzed: ${summary_data['total_revenue']:,.0f}")
            print(f"   - Customer Base: {summary_data['total_customers']} customers")
            print(f"   - Average Order Value: ${summary_data['avg_order_value']:.0f}")
            print(f"   - Top Category: {summary_data['top_category'].title()}")
            
            print(f"\nReady for portfolio presentation!")
            
            return {
                'revenue_data': revenue_data,
                'segment_data': segment_data,
                'sales_data': sales_data,
                'summary_data': summary_data,
                'showcase_path': showcase_path
            }
            
        except Exception as e:
            print(f"Error generating visualizations: {e}")
            return None
        
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()

def main():
    """Main execution function"""
    dashboard = SalesVisualizationDashboard()
    results = dashboard.generate_all_visualizations()
    
    if results:
        print(f"\nSuccess! Your Sales Performance Analytics visualizations are ready.")
        print(f"Use these professional charts for your portfolio and interviews!")
    else:
        print(f"\nFailed to generate visualizations. Please check the data and try again.")

if __name__ == "__main__":
    main()