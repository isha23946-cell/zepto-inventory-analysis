-- Q1: Average discount and out-of-stock rate by category
SELECT m.category,
       COUNT(*) AS products,
       ROUND(AVG(c.discount_percent), 1) AS avg_discount,
       ROUND(100.0 * SUM(CASE WHEN c.out_of_stock THEN 1 ELSE 0 END) / COUNT(*), 1) AS out_of_stock_pct
FROM category_map m
JOIN zepto_clean c ON c.product_id = m.product_id
GROUP BY m.category
ORDER BY avg_discount DESC;

-- Q2: Top 10 products by estimated inventory value (selling price x available quantity)
SELECT product_name, primary_category, selling_price, available_qty, inventory_value
FROM zepto_clean
ORDER BY inventory_value DESC
LIMIT 10;

-- Q3: Cheapest and priciest products per 100 g (weight_g has mixed units, so read with care)
(SELECT 'Cheapest' AS type, product_name, weight_g, selling_price, price_per_100g
 FROM zepto_clean WHERE price_per_100g IS NOT NULL ORDER BY price_per_100g ASC LIMIT 5)
UNION ALL
(SELECT 'Priciest', product_name, weight_g, selling_price, price_per_100g
 FROM zepto_clean WHERE price_per_100g IS NOT NULL ORDER BY price_per_100g DESC LIMIT 5);

-- Q4: Out-of-stock and low-stock rate by discount band
SELECT discount_band,
       COUNT(*) AS products,
       ROUND(100.0 * SUM(CASE WHEN out_of_stock THEN 1 ELSE 0 END) / COUNT(*), 1) AS out_of_stock_pct,
       ROUND(100.0 * SUM(CASE WHEN stock_status = 'Low stock' THEN 1 ELSE 0 END) / COUNT(*), 1) AS low_stock_pct
FROM zepto_clean
GROUP BY discount_band
ORDER BY MIN(discount_percent);
