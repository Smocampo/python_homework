import sqlite3
import pandas as pd

# Hardcoding the exact absolute path to guarantee it connects to the real file
db_path = "/Users/sofiaocampo-morales/Documents/CODE THE DREAM/PYTHON 26.2 CTD/python_class/db/lesson.db"

# Establish connection
conn = sqlite3.connect(db_path)

print("==========================================")
print("STEP 2 & 3: Reading SQL JOIN into DataFrame")
print("==========================================")
query = """
    SELECT 
        line_items.line_item_id, 
        line_items.quantity, 
        products.product_id, 
        products.product_name, 
        products.price
    FROM line_items
    INNER JOIN products ON line_items.product_id = products.product_id;
"""

df = pd.read_sql_query(query, conn)
print(df.head())

print("\n==========================================")
print("STEP 4: Adding 'total' Column (qty * price)")
print("==========================================")
df['total'] = df['quantity'] * df['price']
print(df.head())

print("\n==========================================")
print("STEP 5 & 6: Groupby, Aggregation, and Sorting")
print("==========================================")
summary_df = df.groupby('product_id').agg(
    line_item_id_count=('line_item_id', 'count'),
    total_sum=('total', 'sum'),
    product_name=('product_name', 'first')
).reset_index()

summary_df = summary_df.rename(columns={
    'line_item_id_count': 'order_count',
    'total_sum': 'total_revenue'
})

summary_df = summary_df.sort_values(by='product_name')
print(summary_df.head())

print("\n==========================================")
print("STEP 7: Writing to order_summary.csv")
print("==========================================")
csv_filename = "order_summary.csv"
summary_df.to_csv(csv_filename, index=False)
print(f"Successfully generated and saved '{csv_filename}'!")

conn.close()
