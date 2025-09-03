-- ================================================================
-- Query 3: Product Performance Ranking [MEDIUM]
-- ================================================================
-- Business Question: Which products perform best within their categories, 
-- considering both rating and stock movement potential?
-- 
-- This query ranks products within categories and creates performance
-- scores to identify top performers for promotion and investment.
--
-- Expected Insights:
-- - Top-rated products per category
-- - Products with highest revenue potential
-- - Overall performance leaders
-- - Products suitable for featured promotions
-- ================================================================

-- Product Performance with Category Rankings
SELECT 
    category,
    title as product_name,
    brand,
    price,
    rating,
    stock,
    discountPercentage as discount_pct,
    
    -- Ranking products within their category by rating
    RANK() OVER (PARTITION BY category ORDER BY rating DESC) as rating_rank,
    
    -- Ranking by potential sales (price * stock)
    RANK() OVER (PARTITION BY category ORDER BY (price * stock) DESC) as revenue_potential_rank,
    
    -- Overall performance score combining rating and stock
    ROUND(rating * stock, 2) as performance_score,
    
    -- Revenue potential calculation
    ROUND(price * stock, 2) as revenue_potential
    
FROM products 
WHERE stock > 0 
    AND rating >= 4.0  -- Only high-rated products
ORDER BY category, rating_rank;

-- ================================================================
-- Top Performers Across All Categories
-- ================================================================
SELECT 
    'TOP 10 OVERALL PERFORMERS' as analysis_type,
    title as product_name,
    category,
    brand,
    price,
    rating,
    stock,
    ROUND(rating * stock, 2) as performance_score,
    ROUND(price * stock, 2) as revenue_potential
FROM products 
WHERE stock > 0 AND rating >= 4.0
ORDER BY (rating * stock) DESC
LIMIT 10;

-- ================================================================
-- Category Champions (Best Product per Category)
-- ================================================================
SELECT 
    p1.category,
    p1.title as champion_product,
    p1.brand,
    p1.price,
    p1.rating,
    p1.stock,
    ROUND(p1.rating * p1.stock, 2) as performance_score
FROM products p1
WHERE p1.rating = (
    SELECT MAX(p2.rating) 
    FROM products p2 
    WHERE p2.category = p1.category 
    AND p2.stock > 0
)
AND p1.stock > 0
ORDER BY p1.category;

-- ================================================================
-- Performance Analysis Summary
-- ================================================================
SELECT 
    category,
    COUNT(*) as total_products,
    COUNT(CASE WHEN rating >= 4.5 THEN 1 END) as excellent_products,
    COUNT(CASE WHEN rating >= 4.0 AND rating < 4.5 THEN 1 END) as good_products,
    ROUND(AVG(rating), 2) as avg_category_rating,
    ROUND(AVG(price * stock), 2) as avg_revenue_potential
FROM products 
WHERE stock > 0
GROUP BY category
ORDER BY avg_category_rating DESC;

-- ================================================================
-- Expected Business Impact:
-- - Identify products for featured promotions
-- - Guide inventory investment decisions
-- - Optimize product placement strategies
-- - Focus marketing efforts on proven performers
-- - Plan seasonal promotions around top products
-- ================================================================

-- ================================================================
-- SQL Concepts Demonstrated:
-- - Window functions (RANK, PARTITION BY)
-- - Multiple ORDER BY criteria in window functions
-- - Complex WHERE conditions with AND/OR logic
-- - Subqueries for finding maximum values
-- - Conditional counting with CASE statements
-- - LIMIT for top-N analysis
-- - Correlated subqueries for category-specific analysis
-- ================================================================