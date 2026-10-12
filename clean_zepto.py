"""
Zepto inventory data cleaning
Input : zepto_raw.csv   (Sheet1 of zepto_v1.xlsx exported as CSV)
Output: zepto_clean.csv        one row per unique product
        zepto_category_map.csv every (product_id, category) pair seen in the raw data
"""
import sys
import numpy as np
import pandas as pd

RAW = sys.argv[1] if len(sys.argv) > 1 else "zepto_raw.csv"

df = pd.read_csv(RAW)
print(f"Raw rows: {len(df):,}")

# 1. Standardise column names -> snake_case
df = df.rename(columns={
    "Category": "category",
    "name": "product_name",
    "mrp": "mrp_paise",
    "discountPercent": "discount_percent",
    "availableQuantity": "available_qty",
    "discountedSellingPrice": "selling_price_paise",
    "weightInGms": "weight_g",
    "outOfStock": "out_of_stock",
    "quantity": "pack_size",
})
df["product_name"] = df["product_name"].str.strip().str.strip('"').str.strip()
df["category"] = df["category"].str.strip()
df["out_of_stock"] = df["out_of_stock"].astype(bool)

# 2. Drop rows with no price (MRP or selling price = 0)
bad_price = (df["mrp_paise"] == 0) | (df["selling_price_paise"] == 0)
print(f"Dropping {bad_price.sum()} row(s) with zero price")
df = df[~bad_price].copy()

# 3. Prices: paise -> rupees
df["mrp"] = df["mrp_paise"] / 100
df["selling_price"] = df["selling_price_paise"] / 100
df = df.drop(columns=["mrp_paise", "selling_price_paise"])

# 4. Weight of 0 is missing data, not a real weight
df["weight_g"] = df["weight_g"].replace(0, np.nan)

# 5. The same product is listed under several categories in the raw file.
#    Keep a mapping table of every category it appears under, then keep ONE
#    row per product. "primary_category" is just the first one in the file
#    (an arbitrary tie-break), so use zepto_category_map.csv for any
#    category-level analysis.
product_cols = ["product_name", "mrp", "discount_percent", "available_qty",
                "selling_price", "weight_g", "out_of_stock", "pack_size"]
df["product_id"] = df.groupby(product_cols, dropna=False).ngroup() + 1

category_map = (df[["product_id", "category"]]
                .drop_duplicates()
                .sort_values(["product_id", "category"]))

cats_listed = category_map.groupby("product_id")["category"].nunique().rename("categories_listed")

before = len(df)
df = df.drop_duplicates(subset="product_id", keep="first")
df = df.rename(columns={"category": "primary_category"}).merge(cats_listed, on="product_id")
print(f"Removed {before - len(df):,} duplicate rows -> {len(df):,} unique products")

# 6. Derived columns used in the analysis
df["discount_amount"] = (df["mrp"] - df["selling_price"]).round(2)
df["price_per_100g"] = (df["selling_price"] / df["weight_g"] * 100).round(2)
df["inventory_value"] = (df["available_qty"] * df["selling_price"]).round(2)
df["discount_band"] = pd.cut(
    df["discount_percent"],
    bins=[-1, 0, 10, 20, 100],
    labels=["No discount", "1-10%", "11-20%", "20%+"],
)
df["stock_status"] = np.select(
    [df["out_of_stock"], df["available_qty"] <= 2],
    ["Out of stock", "Low stock"],
    default="In stock",
)

cols = ["product_id", "primary_category", "categories_listed", "product_name", "mrp", "selling_price",
        "discount_percent", "discount_amount", "discount_band", "weight_g",
        "price_per_100g", "pack_size", "available_qty", "out_of_stock",
        "stock_status", "inventory_value"]
df = df[cols].sort_values("product_id")

# 7. Sanity checks
assert df["product_id"].is_unique
assert (df["selling_price"] <= df["mrp"]).all()
assert df.drop(columns=["weight_g", "price_per_100g"]).notna().all().all()

df.to_csv("zepto_clean.csv", index=False)
category_map.to_csv("zepto_category_map.csv", index=False)
print(f"Saved zepto_clean.csv ({len(df):,} rows) and zepto_category_map.csv ({len(category_map):,} rows)")
print(df["stock_status"].value_counts().to_string())
