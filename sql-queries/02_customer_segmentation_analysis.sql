-- ================================================================
-- Query 2: Customer Segmentation Analysis [EASY-MEDIUM]
-- ================================================================
-- Business Question: How can we segment our customers by demographics for targeted marketing?
-- 
-- This query creates meaningful customer segments based on age groups
-- and analyzes their distribution and characteristics.
--
-- Expected Insights:
-- - Customer distribution across generational segments
-- - Average age per segment
-- - Segment sizes for marketing campaign planning
-- - Demographic trends for product targeting
-- ================================================================

-- Customer Segmentation by Age Groups
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
    -- Calculate percentage of total customer base
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
-- Additional Analysis: Gender Distribution by Age Segment
-- ================================================================
SELECT 
    CASE 
        WHEN age < 25 THEN 'Gen Z (Under 25)'
        WHEN age BETWEEN 25 AND 35 THEN 'Millennials (25-35)'
        WHEN age BETWEEN 36 AND 50 THEN 'Gen X (36-50)'
        ELSE 'Boomers (50+)'
    END as age_segment,
    gender,
    COUNT(*) as customer_count,
    ROUND(AVG(age), 1) as avg_age
FROM users 
GROUP BY 
    CASE 
        WHEN age < 25 THEN 'Gen Z (Under 25)'
        WHEN age BETWEEN 25 AND 35 THEN 'Millennials (25-35)'
        WHEN age BETWEEN 36 AND 50 THEN 'Gen X (36-50)'
        ELSE 'Boomers (50+)'
    END,
    gender
ORDER BY age_segment, gender;

-- ================================================================
-- Customer Demographics Summary
-- ================================================================
SELECT 
    'CUSTOMER OVERVIEW' as analysis_type,
    COUNT(*) as total_customers,
    ROUND(AVG(age), 1) as avg_customer_age,
    MIN(age) as youngest_customer,
    MAX(age) as oldest_customer,
    COUNT(DISTINCT gender) as gender_categories
FROM users;

-- ================================================================
-- Expected Business Impact:
-- - Enable targeted marketing campaigns by generation
-- - Optimize product recommendations for age groups
-- - Plan inventory based on demographic preferences
-- - Design age-appropriate marketing messages
-- - Allocate marketing budget by segment size
-- ================================================================

-- ================================================================
-- SQL Concepts Demonstrated:
-- - CASE WHEN statements for conditional logic
-- - Multiple GROUP BY columns
-- - Subqueries for percentage calculations
-- - ROUND function for clean presentation
-- - Complex conditional segmentation logic
-- - Demographic analysis techniques
-- ================================================================