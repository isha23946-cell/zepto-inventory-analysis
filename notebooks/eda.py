import pandas as pd

products = pd.read_csv('data/zepto_clean.csv')
cat_map = pd.read_csv('data/zepto_category_map.csv')
print('products:', products.shape)
print('category pairs:', cat_map.shape)
assert len(products) == 1800
assert len(cat_map) == 3729
print('Row counts match the SQL tables.')
print(products['stock_status'].value_counts())

joined = cat_map.merge(products, on='product_id')
q1 = joined.groupby('category').agg(products=('product_id', 'count'), avg_discount=('discount_percent', 'mean'), out_of_stock_pct=('out_of_stock', lambda s: s.mean() * 100)).round(1).sort_values('avg_discount', ascending=False)
print(q1)
assert q1.loc['Fruits & Vegetables', 'avg_discount'] == 15.5
assert q1.loc['Biscuits', 'out_of_stock_pct'] == 28.6
print('Python matches SQL for Q1.')

band_order = ['No discount', '1-10%', '11-20%', '20%+']
q4 = products.groupby('discount_band').agg(products=('product_id', 'count'), out_of_stock_pct=('out_of_stock', lambda s: s.mean() * 100), low_stock_pct=('stock_status', lambda s: (s == 'Low stock').mean() * 100)).round(1).reindex(band_order)
print(q4)
assert q4.loc['No discount', 'out_of_stock_pct'] == 16.0
assert q4.loc['11-20%', 'out_of_stock_pct'] == 6.1
print('Python matches SQL for Q4.')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
clean_cats = ['Fruits & Vegetables', 'Meats, Fish & Eggs', 'Biscuits', 'Health & Hygiene', 'Home & Cleaning']
c = q1.loc[clean_cats].sort_values('avg_discount')
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(c.index, c['avg_discount'], color='#4C72B0')
ax.set_title('Average discount by category (%)')
ax.set_xlabel('Average discount (%)')
for i, v in enumerate(c['avg_discount']): ax.text(v + 0.2, i, str(v), va='center')
plt.tight_layout()
plt.savefig('images/avg_discount_by_category.png', dpi=150)
plt.close()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(q4.index, q4['out_of_stock_pct'], color='#55A868')
ax.set_title('Out-of-stock rate by discount band')
ax.set_xlabel('Discount band')
ax.set_ylabel('Products out of stock (%)')
for i, v in enumerate(q4['out_of_stock_pct']): ax.text(i, v + 0.3, str(v), ha='center')
plt.tight_layout()
plt.savefig('images/out_of_stock_by_discount_band.png', dpi=150)
plt.close()
print('Charts saved to images/')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
clean_cats = ['Fruits & Vegetables', 'Meats, Fish & Eggs', 'Biscuits', 'Health & Hygiene', 'Home & Cleaning']
c = q1.loc[clean_cats].sort_values('avg_discount')
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(c.index, c['avg_discount'], color='#4C72B0')
ax.set_title('Average discount by category (%)')
ax.set_xlabel('Average discount (%)')
for i, v in enumerate(c['avg_discount']): ax.text(v + 0.2, i, str(v), va='center')
plt.tight_layout()
plt.savefig('images/avg_discount_by_category.png', dpi=150)
plt.close()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(q4.index, q4['out_of_stock_pct'], color='#55A868')
ax.set_title('Out-of-stock rate by discount band')
ax.set_xlabel('Discount band')
ax.set_ylabel('Products out of stock (%)')
for i, v in enumerate(q4['out_of_stock_pct']): ax.text(i, v + 0.3, str(v), ha='center')
plt.tight_layout()
plt.savefig('images/out_of_stock_by_discount_band.png', dpi=150)
plt.close()
print('Charts saved to images/')
