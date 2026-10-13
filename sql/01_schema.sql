-- Zepto project: table definitions
DROP TABLE IF EXISTS category_map;
DROP TABLE IF EXISTS zepto_clean;

CREATE TABLE zepto_clean (
    product_id        INT PRIMARY KEY,
    primary_category  TEXT,
    categories_listed INT,
    product_name      TEXT,
    mrp               NUMERIC(10,2),
    selling_price     NUMERIC(10,2),
    discount_percent  NUMERIC(5,2),
    discount_amount   NUMERIC(10,2),
    discount_band     TEXT,
    weight_g          NUMERIC(10,2),
    price_per_100g    NUMERIC(12,2),
    pack_size         INT,
    available_qty     INT,
    out_of_stock      BOOLEAN,
    stock_status      TEXT,
    inventory_value   NUMERIC(12,2)
);

CREATE TABLE category_map (
    product_id INT REFERENCES zepto_clean(product_id),
    category   TEXT,
    PRIMARY KEY (product_id, category)
);
