-- ================================================================
-- Query 5: Advanced Customer Purchase Analysis [MEDIUM-HARD]
-- ================================================================
-- Business Question: Which customers show the best purchasing patterns 
-- and should be prioritized for retention strategies?
-- 
-- This query analyzes customer behavior patterns, purchase frequency,
-- and value segmentation for targeted marketing and retention programs.
--
-- Expected Insights:
-- - Customer value segmentation
-- - Purchase behavior patterns
-- - Customer lifetime value indicators
-- - Retention strategy targets
-- ================================================================

-- Advanced Customer Purchase Pattern Analysis
SELECT 
    u.firstName,
    u.lastName,
    u.age,
    
    -- Age group classification
    CASE 
        WHEN u.age < 30 THEN 'Young Adult'
        WHEN u.age BETWEEN 30 AND 45 THEN 'Prime Adult'  
        ELSE 'Mature Adult'
    END as age_group,
    
    -- Purchase behavior metrics
    COUNT(DISTINCT c.id) as total_orders,
    ROUND(AVG(c.total), 2) as avg_order_value,
    ROUND(SUM(c.total), 2) as total_spent,
    SUM(c.totalQuantity) as total_items_bought,
    
    -- Purchase frequency analysis
    CASE 
        WHEN COUNT(DISTINCT c.id) >= 3 THEN 'Frequent Buyer'
        WHEN COUNT(DISTINCT c.id) = 2 THEN 'Repeat Customer'
        ELSE 'One-Time Buyer'
    END as purchase_frequency,
    
    -- Value segmentation
    CASE 
        WHEN SUM(c.total) >= 1500 AND COUNT(DISTINCT c.id) >= 3 THEN 'Premium Customer'
        WHEN SUM(c.total) >= 800 AND COUNT(DISTINCT c.id) >= 2 THEN 'Valuable Customer'
        WHEN SUM(c.total) >= 400 OR COUNT(DISTINCT c.id) >= 2 THEN 'Regular Customer'
        ELSE 'Low-Value Customer'
    END as customer_value_segment,
    
    -- Efficiency metrics
    ROUND(SUM(c.total) / COUNT(DISTINCT c.id), 2) as revenue_per_order,
    ROUND(SUM(c.totalQuantity) / COUNT(DISTINCT c.id), 1) as items_per_order

FROM users u
INNER JOIN carts c ON u.id = c.userId
WHERE c.total > 0  -- Only actual purchases
GROUP BY u.id, u.firstName, u.lastName, u.age
HAVING COUNT(DISTINCT c.id) >= 1  -- At least one order
    AND SUM(c.total) >= 100  -- Minimum spend threshold
ORDER BY total_spent DESC, total_orders DESC;

-- ================================================================
-- Customer Segment Summary Analysis
-- ================================================================
SELECT 
    CASE 
        WHEN SUM(c.total) >= 1500 AND COUNT(DISTINCT c.id) >= 3 THEN 'Premium Customer'
        WHEN SUM(c.total) >= 800 AND COUNT(DISTINCT c.id) >= 2 THEN 'Valuable Customer'
        WHEN SUM(c.total) >= 400 OR COUNT(DISTINCT c.id) >= 2 THEN 'Regular Customer'
        ELSE 'Low-Value Customer'
    END as customer_segment,
    
    COUNT(DISTINCT u.id) as customer_count,
    ROUND(AVG(SUM(c.total)), 2) as avg_customer_value,
    ROUND(SUM(SUM(c.total)), 2) as segment_total_value,
    ROUND(AVG(COUNT(DISTINCT c.id)), 1) as avg_orders_per_customer,
    ROUND(AVG(AVG(c.total)), 2) as avg_order_value_in_segment
    
FROM users u
INNER JOIN carts c ON u.id = c.userId
WHERE c.total > 0
GROUP BY u.id
GROUP BY 
    CASE 
        WHEN SUM(c.total) >= 1500 AND COUNT(DISTINCT c.id) >= 3 THEN 'Premium Customer'
        WHEN SUM(c.total) >= 800 AND COUNT(DISTINCT c.id) >= 2 THEN 'Valuable Customer'
        WHEN SUM(c.total) >= 400 OR COUNT(DISTINCT c.id) >= 2 THEN 'Regular Customer'
        ELSE 'Low-Value Customer'
    END
ORDER BY avg_customer_value DESC;

-- ================================================================
-- Age Group Purchase Behavior
-- ================================================================
SELECT 
    CASE 
        WHEN u.age < 30 THEN 'Young Adult'
        WHEN u.age BETWEEN 30 AND 45 THEN 'Prime Adult'  
        ELSE 'Mature Adult'
    END as age_group,
    
    COUNT(DISTINCT u.id) as customers_in_group,
    ROUND(AVG(u.age), 1) as avg_age,
    COUNT(DISTINCT c.id) as total_orders,
    ROUND(AVG(c.total), 2) as avg_order_value,
    ROUND(SUM(c.total), 2) as total_group_spending,
    ROUND(SUM(c.total) / COUNT(DISTINCT u.id), 2) as spending_per_customer
    
FROM users u
INNER JOIN carts c ON u.id = c.userId
WHERE c.total > 0
GROUP BY 
    CASE 
        WHEN u.age < 30 THEN 'Young Adult'
        WHEN u.age BETWEEN 30 AND 45 THEN 'Prime Adult'  
        ELSE 'Mature Adult'
    END
ORDER BY spending_per_customer DESC;

-- ================================================================
-- High-Value Customer Details (Top 10)
-- ================================================================
SELECT 
    'TOP 10 CUSTOMERS BY VALUE' as analysis_type,
    u.firstName || ' ' || u.lastName as customer_name,
    u.age,
    COUNT(DISTINCT c.id) as total_orders,
    ROUND(SUM(c.total), 2) as total_lifetime_value,
    ROUND(AVG(c.total), 2) as avg_order_value,
    SUM(c.totalQuantity) as total_items_purchased
FROM users u
INNER JOIN carts c ON u.id = c.userId
WHERE c.total > 0
GROUP BY u.id, u.firstName, u.lastName, u.age
ORDER BY SUM(c.total) DESC
LIMIT 10;

-- ================================================================
-- Customer Retention Analysis
-- ================================================================
SELECT 
    COUNT(DISTINCT u.id) as total_active_customers,
    COUNT(DISTINCT CASE WHEN order_count >= 2 THEN u.id END) as repeat_customers,
    COUNT(DISTINCT CASE WHEN order_count >= 3 THEN u.id END) as frequent_customers,
    
    ROUND(
        COUNT(DISTINCT CASE WHEN order_count >= 2 THEN u.id END) * 100.0 / 
        COUNT(DISTINCT u.id), 2
    ) as repeat_customer_rate,
    
    ROUND(AVG(customer_value), 2) as avg_customer_lifetime_value
    
FROM (
    SELECT 
        u.id,
        COUNT(DISTINCT c.id) as order_count,
        SUM(c.total) as customer_value
    FROM users u
    INNER JOIN carts c ON u.id = c.userId
    WHERE c.total > 0
    GROUP BY u.id
) customer_summary
CROSS JOIN users u
WHERE u.id IN (
    SELECT DISTINCT userId FROM carts WHERE total > 0
);

-- ================================================================
-- Expected Business Impact:
-- - Identify high-value customers for VIP programs
-- - Design targeted retention campaigns
-- - Optimize marketing spend by customer segment
-- - Plan loyalty programs based on purchase patterns
-- - Focus customer service resources on valuable segments
-- ================================================================

-- ================================================================
-- SQL Concepts Demonstrated:
-- - INNER JOIN for connecting related tables
-- - Multiple CASE statements for complex segmentation
-- - Mixed aggregation functions (COUNT DISTINCT, SUM, AVG)
-- - HAVING clause for post-aggregation filtering
-- - String concatenation with || operator
-- - Nested aggregations and complex business logic
-- - LIMIT for top-N analysis
-- - Subqueries for complex calculations
-- ================================================================