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

**Technical Implementation:**
- Advanced data aggregation and business metrics
- Strategic grouping and performance ordering
- Complex analytical subqueries

---

### 2. `02_customer_segmentation_analysis.sql` [EASY-MEDIUM]
**Business Question:** How can we segment customers for targeted marketing?

**Key Metrics:**
- Age-based customer segmentation
- Demographic distribution analysis
- Gender analysis by age group
- Customer base percentages

**Technical Implementation:**
- Advanced conditional business logic
- Multi-dimensional analytical processing
- Strategic demographic intelligence

---

### 3. `03_product_performance_ranking.sql` [MEDIUM]
**Business Question:** Which products perform best within their categories?

**Key Metrics:**
- Product rankings by rating and revenue
- Performance scoring system
- Category champions identification
- Top performers analysis

**Technical Implementation:**
- Advanced window functions and competitive ranking
- Multi-criteria performance analysis systems
- Complex analytical query architecture
- Strategic performance scoring algorithms

---

### 4. `04_category_performance_analysis.sql` [MEDIUM]
**Business Question:** How do categories perform across price ranges?

**Key Metrics:**
- Price segmentation analysis
- Stock level distribution
- Market share calculations
- Revenue potential by price tier

**Technical Implementation:**
- Advanced segmentation logic and conditional processing
- Enterprise-grade aggregation methodologies
- Strategic conditional analytics
- Complex business intelligence implementation

---

### 5. `05_advanced_customer_analysis.sql` [MEDIUM-HARD]
**Business Question:** Which customers should be prioritized for retention?

**Key Metrics:**
- Customer lifetime value analysis
- Purchase behavior patterns
- Customer value segmentation
- Retention analytics

**Technical Implementation:**
- Multi-table data integration and cross-functional analysis
- Advanced customer intelligence segmentation
- Strategic business value calculations
- Comprehensive behavioral analytics framework

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

## 🎯 Business Intelligence Framework

### Strategic Analytics Approach:
- **Data-Driven Insights:** Business problems solved through advanced SQL analytics
- **Scalable Methodology:** From foundational analysis to complex business intelligence
- **Executive Focus:** Actionable insights that drive strategic decision making
- **Complete Pipeline:** Data integration → analytical processing → strategic recommendations

### Technical Documentation:
Each query includes comprehensive business context:
- **Strategic objectives** and business requirements
- **Analytical methodology** and implementation logic
- **Technical architecture** and data processing techniques
- **Business impact** and strategic value proposition

## 💼 Professional Applications

These analyses are directly applicable to:
- **E-commerce companies** (product and customer analytics)
- **Retail businesses** (inventory and sales optimization)
- **Marketing agencies** (customer segmentation and targeting)
- **Business intelligence roles** (KPI development and reporting)
- **Data analyst positions** (revenue analysis and forecasting)

## 🔧 Technical Implementation Architecture

**Foundation Layer (Queries 1-2):**
- Core data aggregation and business metrics calculation
- Fundamental business intelligence reporting
- Strategic performance indicator development

**Strategic Layer (Queries 3-4):**
- Advanced analytical functions and competitive ranking systems
- Complex business segmentation logic
- Multi-dimensional performance analysis

**Executive Layer (Query 5):**
- Comprehensive cross-functional data integration
- Advanced customer intelligence algorithms
- Strategic business intelligence and predictive analytics

---

**Technical Specifications:** Professional Business Intelligence SQL Suite  
**Implementation:** Advanced Analytics with Strategic Business Applications  
**Architecture:** Enterprise-Grade SQLite Data Processing Pipeline