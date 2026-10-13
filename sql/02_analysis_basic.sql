-- Q1: Average discount and out-of-stock rate by category
SELECT m.category,
       COUNT(*) AS products,
       ROUND(AVG(c.discount_percent), 1) AS avg_discount,
       ROUND(100.0 * SUM(CASE WHEN c.out_of_stock THEN 1 ELSE 0 END) / COUNT(*), 1) AS out_of_stock_pct
FROM category_map m
JOIN zepto_clean c ON c.product_id = m.product_id
GROUP BY m.category
ORDER BY avg_discount DESC;
