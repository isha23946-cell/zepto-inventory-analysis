-- Q5: Top 3 most discounted products in each of the five cleanest categories (CTE + window function)
WITH ranked AS (
    SELECT m.category, c.product_name, c.mrp, c.selling_price, c.discount_percent,
           ROW_NUMBER() OVER (PARTITION BY m.category
                              ORDER BY c.discount_percent DESC, c.discount_amount DESC) AS rn
    FROM category_map m
    JOIN zepto_clean c ON c.product_id = m.product_id
    WHERE m.category IN ('Fruits & Vegetables', 'Meats, Fish & Eggs', 'Biscuits', 'Health & Hygiene', 'Home & Cleaning')
)
SELECT category, rn AS rank_in_category, product_name, mrp, selling_price, discount_percent
FROM ranked
WHERE rn <= 3
ORDER BY category, rn;

-- Q6: Heavily discounted products (20%+) that are low on stock or out of stock
SELECT product_name, primary_category, mrp, selling_price, discount_percent, available_qty, stock_status
FROM zepto_clean
WHERE discount_percent >= 20
  AND stock_status IN ('Out of stock', 'Low stock')
ORDER BY discount_percent DESC, mrp DESC
LIMIT 15;
