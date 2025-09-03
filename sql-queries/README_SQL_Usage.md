# 📊 SQL Queries Usage Guide

## Sales Performance Analytics - SQL Analysis Suite

This folder contains 5 comprehensive SQL analysis queries designed to extract actionable business insights from the sales performance data extracted via the DummyJSON API.

## 🔧 Database Setup

**Database Type:** SQLite  
**Database File:** `../data/sales_data.db`  
**Tables Available:**
- `products` - Product catalog with pricing, ratings, stock
- `users` - Customer demographic information  
- `carts` - Transaction data with totals and discounts
- `cart_items` - Detailed purchase line items

## 📋 Query Files Overview

### 1. `01_revenue_analysis_by_category.sql` [EASY]
**Business Question:** Which product categories are our biggest revenue drivers?

**Key Metrics:**
- Revenue potential by category
- Average prices per category
- Product count and availability
- Category performance ratings

**Skills Demonstrated:**
- Basic aggregation (COUNT, SUM, AVG)
- GROUP BY and ORDER BY
- Subqueries for percentages

---

### 2. `02_customer_segmentation_analysis.sql` [EASY-MEDIUM]
**Business Question:** How can we segment customers for targeted marketing?

**Key Metrics:**
- Age-based customer segmentation
- Demographic distribution analysis
- Gender analysis by age group
- Customer base percentages

**Skills Demonstrated:**
- CASE WHEN conditional logic
- Complex GROUP BY operations
- Demographic analysis techniques

---

### 3. `03_product_performance_ranking.sql` [MEDIUM]
**Business Question:** Which products perform best within their categories?

**Key Metrics:**
- Product rankings by rating and revenue
- Performance scoring system
- Category champions identification
- Top performers analysis

**Skills Demonstrated:**
- Window functions (RANK, PARTITION BY)
- Multiple ranking criteria
- Correlated subqueries
- Performance scoring algorithms

---

### 4. `04_category_performance_analysis.sql` [MEDIUM]
**Business Question:** How do categories perform across price ranges?

**Key Metrics:**
- Price segmentation analysis
- Stock level distribution
- Market share calculations
- Revenue potential by price tier

**Skills Demonstrated:**
- Complex CASE statements for segmentation
- Multiple aggregation functions
- Conditional counting
- Business logic implementation

---

### 5. `05_advanced_customer_analysis.sql` [MEDIUM-HARD]
**Business Question:** Which customers should be prioritized for retention?

**Key Metrics:**
- Customer lifetime value analysis
- Purchase behavior patterns
- Customer value segmentation
- Retention analytics

**Skills Demonstrated:**
- INNER JOINs across multiple tables
- Complex customer segmentation
- Advanced business calculations
- Customer behavior analysis

---

### 6. `run_all_analyses.sql` [MASTER FILE]
**Purpose:** Comprehensive analysis suite with executive summary

**Includes:**
- All 5 analyses in one file
- Executive summary dashboard
- Key business recommendations
- Strategic insights compilation

## 🚀 How to Execute These Queries

### Option 1: SQLite Command Line
```bash
# Navigate to data directory
cd ../data

# Run individual query
sqlite3 sales_data.db < ../sql-queries/01_revenue_analysis_by_category.sql

# Run complete analysis
sqlite3 sales_data.db < ../sql-queries/run_all_analyses.sql
```

### Option 2: DB Browser for SQLite
1. Download and install DB Browser for SQLite
2. Open `../data/sales_data.db`
3. Copy and paste queries from files
4. Execute and export results

### Option 3: Python Integration
```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('../data/sales_data.db')

# Read and execute query
with open('../sql-queries/01_revenue_analysis_by_category.sql', 'r') as f:
    query = f.read()
    
df = pd.read_sql_query(query, conn)
print(df)
```

### Option 4: Excel/Power BI
1. Open Excel or Power BI
2. Connect to SQLite database
3. Import queries as data sources
4. Create dashboards and visualizations

## 📊 Expected Results Summary

### Key Business Insights:
- **Revenue Leaders:** Electronics and beauty categories likely top performers
- **Customer Segments:** Millennials (25-35) probably largest segment
- **Product Stars:** Premium products with 4.5+ ratings perform best
- **Price Strategy:** Mid-range ($50-$200) products may dominate sales
- **Customer Value:** 80/20 rule - top 20% customers drive 80% revenue

### Actionable Recommendations:
1. **Focus marketing budget** on highest revenue categories
2. **Develop retention programs** for high-value customers
3. **Optimize inventory** for top-performing products
4. **Target millennial segment** with age-appropriate campaigns
5. **Consider premium pricing** for highly-rated products

## 🎯 Portfolio Value Proposition

### For Entry-Level DA Roles:
- **Practical SQL Skills:** Real business problems solved with SQL
- **Progressive Complexity:** From basic aggregation to advanced analytics
- **Business Acumen:** Focus on actionable insights, not just technical execution
- **End-to-End Process:** API extraction → SQL analysis → business recommendations

### Interview Preparation:
Each query includes detailed comments explaining:
- **Business context** and objectives
- **Step-by-step logic** breakdown
- **SQL concepts demonstrated**
- **Expected business impact**

## 💼 Professional Applications

These analyses are directly applicable to:
- **E-commerce companies** (product and customer analytics)
- **Retail businesses** (inventory and sales optimization)
- **Marketing agencies** (customer segmentation and targeting)
- **Business intelligence roles** (KPI development and reporting)
- **Data analyst positions** (revenue analysis and forecasting)

## 🎓 Skills Progression Demonstrated

**Basic Level (Queries 1-2):**
- SELECT, WHERE, GROUP BY, ORDER BY
- Basic aggregation functions
- Simple business logic

**Intermediate Level (Queries 3-4):**
- Window functions and ranking
- Complex CASE statements
- Subqueries and joins

**Advanced Level (Query 5):**
- Multi-table analysis
- Customer segmentation algorithms
- Business intelligence metrics

---

**Created by:** Salomón Santiago Esquivel  
**Purpose:** Data Analyst Portfolio Project  
**Market:** Entry to Mid-Level DA positions in Mexico  
**Database:** SQLite with DummyJSON API data