-- ================================================================
-- SALES PERFORMANCE ANALYTICS - COMPLETE ANALYSIS SUITE
-- ================================================================
-- Project: Sales Performance Analytics Dashboard
-- Created by: Salomón Santiago Esquivel
-- Data Source: DummyJSON API
-- Database: sales_data.db (SQLite)
--
-- This master file runs all 5 key analyses for comprehensive
-- sales performance insights and business intelligence.
-- ================================================================

-- ================================================================
-- ANALYSIS 1: REVENUE ANALYSIS BY CATEGORY
-- ================================================================
-- Business Focus: Revenue drivers and category performance
SELECT '=== ANALYSIS 1: REVENUE BY CATEGORY ===' as analysis_section;

SELECT 
    category,
    COUNT(*) as total_products,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(SUM(price * stock), 2) as potential_revenue,
    ROUND(AVG(rating), 2) as avg_category_rating,
    ROUND(MIN(price), 2) as min_price,
    ROUND(MAX(price), 2) as max_price,
    SUM(stock) as total_stock_available
FROM products 
WHERE stock > 0
GROUP BY category 
ORDER BY potential_revenue DESC;

-- ================================================================
-- ANALYSIS 2: CUSTOMER SEGMENTATION 
-- ================================================================
-- Business Focus: Customer demographics and targeting
SELECT '=== ANALYSIS 2: CUSTOMER SEGMENTATION ===' as analysis_section;

SELECT 
    CASE 
        WHEN age < 25 THEN 'Gen Z (Under 25)'
        WHEN age BETWEEN 25 AND 35 THEN 'Millennials (25-35)'
        WHEN age BETWEEN 36 AND 50 THEN 'Gen X (36-50)'
        ELSE 'Boomers (50+)'
    END as age_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(age), 1) as avg_age,
    MIN(age) as min_age,
    MAX(age) as max_age,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as percentage_of_total
FROM users 
GROUP BY 
    CASE 
        WHEN age < 25 THEN 'Gen Z (Under 25)'
        WHEN age BETWEEN 25 AND 35 THEN 'Millennials (25-35)'
        WHEN age BETWEEN 36 AND 50 THEN 'Gen X (36-50)'
        ELSE 'Boomers (50+)'
    END
ORDER BY customer_count DESC;

-- ================================================================
-- ANALYSIS 3: PRODUCT PERFORMANCE RANKING
-- ================================================================
-- Business Focus: Top performers and product optimization
SELECT '=== ANALYSIS 3: TOP 10 PRODUCT PERFORMERS ===' as analysis_section;

SELECT 
    category,
    title as product_name,
    brand,
    price,
    rating,
    stock,
    RANK() OVER (PARTITION BY category ORDER BY rating DESC) as category_rank,
    ROUND(rating * stock, 2) as performance_score,
    ROUND(price * stock, 2) as revenue_potential
FROM products 
WHERE stock > 0 AND rating >= 4.0
ORDER BY performance_score DESC
LIMIT 10;

-- ================================================================
-- ANALYSIS 4: PRICE SEGMENTATION ANALYSIS
-- ================================================================
-- Business Focus: Price positioning and market opportunities
SELECT '=== ANALYSIS 4: PRICE SEGMENT PERFORMANCE ===' as analysis_section;

SELECT 
    CASE 
        WHEN price < 50 THEN 'Budget (Under $50)'
        WHEN price BETWEEN 50 AND 200 THEN 'Mid-Range ($50-$200)'
        WHEN price BETWEEN 200 AND 500 THEN 'Premium ($200-$500)'
        ELSE 'Luxury (Over $500)'
    END as price_segment,
    COUNT(*) as product_count,
    COUNT(DISTINCT category) as categories_represented,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(rating), 2) as avg_rating,
    SUM(stock) as total_stock,
    ROUND(SUM(price * stock), 2) as revenue_potential
FROM products 
WHERE rating >= 3.0
GROUP BY 
    CASE 
        WHEN price < 50 THEN 'Budget (Under $50)'
        WHEN price BETWEEN 50 AND 200 THEN 'Mid-Range ($50-$200)'
        WHEN price BETWEEN 200 AND 500 THEN 'Premium ($200-$500)'
        ELSE 'Luxury (Over $500)'
    END
ORDER BY avg_price;

-- ================================================================
-- ANALYSIS 5: CUSTOMER VALUE SEGMENTATION
-- ================================================================
-- Business Focus: Customer lifetime value and retention
SELECT '=== ANALYSIS 5: TOP 10 CUSTOMERS BY VALUE ===' as analysis_section;

SELECT 
    u.firstName || ' ' || u.lastName as customer_name,
    u.age,
    CASE 
        WHEN u.age < 30 THEN 'Young Adult'
        WHEN u.age BETWEEN 30 AND 45 THEN 'Prime Adult'  
        ELSE 'Mature Adult'
    END as age_group,
    COUNT(DISTINCT c.id) as total_orders,
    ROUND(SUM(c.total), 2) as total_lifetime_value,
    ROUND(AVG(c.total), 2) as avg_order_value,
    SUM(c.totalQuantity) as total_items_purchased,
    CASE 
        WHEN SUM(c.total) >= 1500 AND COUNT(DISTINCT c.id) >= 3 THEN 'Premium Customer'
        WHEN SUM(c.total) >= 800 AND COUNT(DISTINCT c.id) >= 2 THEN 'Valuable Customer'
        WHEN SUM(c.total) >= 400 OR COUNT(DISTINCT c.id) >= 2 THEN 'Regular Customer'
        ELSE 'Low-Value Customer'
    END as customer_segment
FROM users u
INNER JOIN carts c ON u.id = c.userId
WHERE c.total > 0
GROUP BY u.id, u.firstName, u.lastName, u.age
ORDER BY SUM(c.total) DESC
LIMIT 10;

-- ================================================================
-- EXECUTIVE SUMMARY - KEY BUSINESS METRICS
-- ================================================================
SELECT '=== EXECUTIVE SUMMARY ===' as analysis_section;

-- Overall Business Metrics
SELECT 
    'BUSINESS OVERVIEW' as metric_type,
    (SELECT COUNT(*) FROM products WHERE stock > 0) as active_products,
    (SELECT COUNT(DISTINCT category) FROM products) as product_categories,
    (SELECT COUNT(*) FROM users) as total_customers,
    (SELECT COUNT(*) FROM carts WHERE total > 0) as total_orders,
    (SELECT ROUND(SUM(total), 2) FROM carts) as total_sales_volume,
    (SELECT ROUND(AVG(total), 2) FROM carts WHERE total > 0) as avg_order_value
;

-- Category Performance Summary  
SELECT 
    'CATEGORY LEADERS' as metric_type,
    (SELECT category FROM products WHERE stock > 0 GROUP BY category ORDER BY SUM(price * stock) DESC LIMIT 1) as top_revenue_category,
    (SELECT category FROM products WHERE stock > 0 GROUP BY category ORDER BY AVG(rating) DESC LIMIT 1) as highest_rated_category,
    (SELECT category FROM products WHERE stock > 0 GROUP BY category ORDER BY COUNT(*) DESC LIMIT 1) as largest_category
;

-- Customer Insights
SELECT 
    'CUSTOMER INSIGHTS' as metric_type,
    (SELECT ROUND(AVG(age), 1) FROM users) as avg_customer_age,
    (SELECT COUNT(*) FROM users WHERE age BETWEEN 25 AND 35) as millennial_customers,
    (SELECT COUNT(DISTINCT u.id) FROM users u JOIN carts c ON u.id = c.userId WHERE c.total > 0 GROUP BY u.id HAVING COUNT(c.id) >= 2) as repeat_customers
;

-- ================================================================
-- RECOMMENDATIONS BASED ON ANALYSIS
-- ================================================================
SELECT '=== KEY RECOMMENDATIONS ===' as analysis_section;

SELECT 
    'STRATEGIC RECOMMENDATIONS' as recommendation_type,
    'Focus marketing budget on highest revenue category' as recommendation_1,
    'Develop retention programs for repeat customers' as recommendation_2,
    'Optimize inventory for high-performing products' as recommendation_3,
    'Target millennial segment (largest customer group)' as recommendation_4,
    'Consider premium pricing strategy for top-rated products' as recommendation_5
;

-- ================================================================
-- ANALYSIS COMPLETE
-- ================================================================
SELECT 'Analysis completed successfully! Ready for visualization and reporting.' as completion_status;

-- ================================================================
-- NEXT STEPS FOR BUSINESS INTELLIGENCE:
-- 1. Export results to Excel for dashboard creation
-- 2. Create Tableau visualizations for stakeholder presentations  
-- 3. Set up automated reporting for ongoing monitoring
-- 4. Implement recommendations and track impact
-- 5. Schedule regular analysis updates with fresh API data
-- ================================================================