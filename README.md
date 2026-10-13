# Zepto Inventory & Pricing Analysis

An end-to-end data analysis project on Zepto product listings, using SQL (PostgreSQL), Python (pandas) and Power BI.

## Business questions
- Which categories offer the deepest discounts?
- Which categories have the most out-of-stock products?
- Where is the most inventory value concentrated?
- Which products give the best value per 100 g?
- Does discount depth relate to stock-outs?

## Dataset
- Source: Zepto product listing data (zepto_v1.xlsx, Sheet1)
- 3,730 rows and 9 columns: category, product name, MRP, discount %, available quantity, selling price, weight (g), out-of-stock flag, pack quantity

## Data cleaning (clean_zepto.py)
- Prices were stored in paise, so I converted MRP and selling price to rupees
- Removed 1 product with a price of 0
- Treated a weight of 0 as missing, not a real weight
- The same product was listed under several categories, so I kept one row per product (3,729 rows reduced to 1,800 unique products) and saved every product-category pair in a separate mapping table
- Added discount_band, stock_status, price_per_100g and inventory_value columns

## Data limitation
Several categories contain exactly the same products (for example Cooking Essentials and Munchies), so those categories cannot be compared reliably. Category-level conclusions focus on categories with distinct product lists.

## Stock status of the 1,800 unique products
- In stock: 1,328
- Low stock (1-2 units): 255
- Out of stock: 217

## Project structure
- data/ : raw and cleaned CSV files
- sql/ : schema and analysis queries
- notebooks/ : Python EDA
- dashboard/ : Power BI file and screenshots
- images/ : charts used in this README
- clean_zepto.py : data cleaning script

## Tools
PostgreSQL, Python (pandas, matplotlib, seaborn), Power BI, Git and GitHub

## Key insights
_To be added after the analysis._

## Recommendations
_To be added after the analysis._
