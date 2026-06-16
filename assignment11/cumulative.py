import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to the database
conn = sqlite3.connect('../db/lesson.db')

# 2. SQL query to get the total price for each order_id
query = """
SELECT 
    o.order_id, 
    SUM(p.price * l.quantity) AS total_price 
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""

# Load the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# 3. Add the "cumulative" column 
df['cumulative'] = df['total_price'].cumsum()

# 4. Use Pandas plotting to create a line plot 
ax = df.plot(
    kind='line', 
    x='order_id', 
    y='cumulative', 
    marker='o',          
    color='darkgreen', 
    linewidth=2,
    legend=False
)

# 5. Add titles and labels
plt.title('Cumulative Revenue Growth Over Orders', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Order ID', fontsize=12, labelpad=10)
plt.ylabel('Cumulative Revenue ($)', fontsize=12, labelpad=10)

# Clean up layout 
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# 6. Show the plot
plt.show()