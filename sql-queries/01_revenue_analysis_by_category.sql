-- ================================================================
-- Query 1: Revenue Analysis by Category [EASY]
-- ================================================================
-- Business Question: Which product categories are our biggest revenue drivers?
-- 
-- This query analyzes revenue potential, product count, and average metrics
-- by category to identify top-performing product segments.
--
-- Expected Insights:
-- - Which categories have the highest revenue potential
-- - Average price points per category  
-- - Product availability and stock levels
-- - Category performance ratings
-- ================================================================

-- Revenue Analysis by Category
SELECT 
    category,
    COUNT(*) as total_products,
    AVG(price) as avg_price,
    SUM(price * stock) as potential_revenue,
    AVG(rating) as avg_category_rating,
    MIN(price) as min_price,
    MAX(price) as max_price,
    SUM(stock) as total_stock_available,
    -- Calculate percentage of total products
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 2) as pct_of_total_products
FROM products 
WHERE stock > 0  -- Only consider products in stock
GROUP BY category 
ORDER BY potential_revenue DESC;

-- ================================================================
-- Expected Business Impact:
-- - Identify high-revenue categories for investment priority
-- - Understand pricing strategies per category
-- - Optimize inventory allocation based on revenue potential
-- - Guide marketing budget allocation to top-performing categories
-- ================================================================

-- Additional Analysis: Category Performance Summary
SELECT 
    'CATEGORY OVERVIEW' as analysis_type,
    COUNT(DISTINCT category) as total_categories,
    COUNT(*) as total_products,
    ROUND(AVG(price), 2) as overall_avg_price,
    SUM(stock) as total_inventory,
    ROUND(AVG(rating), 2) as overall_avg_rating
FROM products
WHERE stock > 0;

-- ================================================================
-- SQL Concepts Demonstrated:
-- - Basic aggregation functions (COUNT, SUM, AVG, MIN, MAX)
-- - GROUP BY for categorical analysis
-- - WHERE clause for filtering
-- - ORDER BY for result ranking
-- - Subquery for percentage calculation
-- - ROUND function for clean number presentation
-- ================================================================