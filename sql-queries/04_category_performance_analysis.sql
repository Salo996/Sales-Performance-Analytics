-- ================================================================
-- Query 4: Category Performance Analysis with Price Segmentation [MEDIUM]
-- ================================================================
-- Business Question: How do different categories perform across price ranges and stock levels?
-- 
-- This query analyzes category performance by price segments to understand
-- market positioning and identify opportunities for optimization.
--
-- Expected Insights:
-- - Price distribution within categories
-- - Stock level patterns by price segment
-- - Revenue potential by price tier
-- - Market share within categories
-- ================================================================

-- Category Performance Analysis with Price Segmentation
SELECT 
    category,
    
    -- Price segmentation
    CASE 
        WHEN price < 50 THEN 'Budget (Under $50)'
        WHEN price BETWEEN 50 AND 200 THEN 'Mid-Range ($50-$200)'
        WHEN price BETWEEN 200 AND 500 THEN 'Premium ($200-$500)'
        ELSE 'Luxury (Over $500)'
    END as price_segment,
    
    COUNT(*) as product_count,
    ROUND(AVG(price), 2) as avg_price_in_segment,
    ROUND(AVG(rating), 2) as avg_rating,
    SUM(stock) as total_stock_available,
    
    -- Stock status analysis
    SUM(CASE WHEN stock < 10 THEN 1 ELSE 0 END) as low_stock_products,
    SUM(CASE WHEN stock >= 50 THEN 1 ELSE 0 END) as high_stock_products,
    
    -- Revenue potential by segment
    ROUND(SUM(price * stock), 2) as revenue_potential,
    
    -- Market share within category
    ROUND(COUNT(*) * 100.0 / 
        (SELECT COUNT(*) FROM products p2 WHERE p2.category = products.category), 2
    ) as pct_of_category

FROM products 
WHERE rating >= 3.0  -- Focus on decent quality products
GROUP BY 
    category, 
    CASE 
        WHEN price < 50 THEN 'Budget (Under $50)'
        WHEN price BETWEEN 50 AND 200 THEN 'Mid-Range ($50-$200)'
        WHEN price BETWEEN 200 AND 500 THEN 'Premium ($200-$500)'
        ELSE 'Luxury (Over $500)'
    END
HAVING COUNT(*) >= 1  -- Show all segments even with one product
ORDER BY category, avg_price_in_segment;

-- ================================================================
-- Price Segment Performance Summary
-- ================================================================
SELECT 
    CASE 
        WHEN price < 50 THEN 'Budget (Under $50)'
        WHEN price BETWEEN 50 AND 200 THEN 'Mid-Range ($50-$200)'
        WHEN price BETWEEN 200 AND 500 THEN 'Premium ($200-$500)'
        ELSE 'Luxury (Over $500)'
    END as price_segment,
    
    COUNT(*) as total_products,
    COUNT(DISTINCT category) as categories_represented,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(rating), 2) as avg_rating,
    SUM(stock) as total_stock,
    ROUND(SUM(price * stock), 2) as total_revenue_potential
    
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
-- Stock Level Analysis by Category
-- ================================================================
SELECT 
    category,
    COUNT(*) as total_products,
    ROUND(AVG(stock), 1) as avg_stock_level,
    MIN(stock) as min_stock,
    MAX(stock) as max_stock,
    
    -- Stock status distribution
    COUNT(CASE WHEN stock < 10 THEN 1 END) as critical_stock_products,
    COUNT(CASE WHEN stock BETWEEN 10 AND 49 THEN 1 END) as moderate_stock_products,
    COUNT(CASE WHEN stock >= 50 THEN 1 END) as high_stock_products,
    
    -- Percentage of products with critical stock
    ROUND(COUNT(CASE WHEN stock < 10 THEN 1 END) * 100.0 / COUNT(*), 2) as critical_stock_percentage
    
FROM products 
GROUP BY category
ORDER BY avg_stock_level DESC;

-- ================================================================
-- Category-Price Matrix Analysis
-- ================================================================
SELECT 
    category,
    ROUND(MIN(price), 2) as lowest_price,
    ROUND(MAX(price), 2) as highest_price,
    ROUND(AVG(price), 2) as average_price,
    ROUND(MAX(price) - MIN(price), 2) as price_range,
    COUNT(*) as product_variety,
    ROUND(AVG(rating), 2) as category_quality_score
FROM products 
WHERE stock > 0
GROUP BY category
ORDER BY price_range DESC;

-- ================================================================
-- Expected Business Impact:
-- - Identify pricing gaps and opportunities
-- - Optimize inventory allocation by price segment
-- - Guide product development for underserved segments
-- - Plan promotional strategies by price tier
-- - Balance portfolio across price ranges
-- ================================================================

-- ================================================================
-- SQL Concepts Demonstrated:
-- - Complex CASE WHEN statements for price segmentation
-- - Multiple aggregation functions in single query
-- - Conditional counting with CASE in aggregations
-- - Correlated subqueries for percentage calculations
-- - HAVING clause for group filtering
-- - GROUP BY with multiple columns including CASE expressions
-- - Business logic implementation in SQL
-- ================================================================