import sqlite3

def main():
    database_path = "../db/lesson.db"
    
    try:
        conn = sqlite3.connect(database_path)
        # Enforce foreign key constraints
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        
        # =====================================================================
        # --- Task 1: Complex JOINs with Aggregation ---
        # =====================================================================
        query_task1 = """
        SELECT 
            orders.order_id, 
            SUM(products.price * line_items.quantity) AS total_price
        FROM orders
        JOIN line_items ON orders.order_id = line_items.order_id
        JOIN products ON line_items.product_id = products.product_id
        GROUP BY orders.order_id
        ORDER BY orders.order_id ASC
        LIMIT 5;
        """
        cursor.execute(query_task1)
        rows_task1 = cursor.fetchall()
        
        print("--- Task 1: Complex JOINs with Aggregation ---")
        for row in rows_task1:
            print(f"Order ID: {row[0]} | Total Price: ${row[1]:.2f}")
            
        print("\n" + "="*50 + "\n")
        
        # =====================================================================
        # --- Task 2: Understanding Subqueries ---
        # =====================================================================
        query_task2 = """
        SELECT 
            customers.customer_name,
            AVG(order_totals.total_price) AS average_total_price
        FROM customers
        LEFT JOIN (
            SELECT 
                orders.customer_id AS customer_id_b,
                SUM(products.price * line_items.quantity) AS total_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
        ) AS order_totals ON customers.customer_id = order_totals.customer_id_b
        GROUP BY customers.customer_id;
        """
        cursor.execute(query_task2)
        rows_task2 = cursor.fetchall()
        
        print("--- Task 2: Understanding Subqueries ---")
        for row in rows_task2:
            avg_price = row[1] if row[1] is not None else 0.0
            print(f"Customer: {row[0]:<20} | Avg Order Value: ${avg_price:.2f}")
            
        print("\n" + "="*50 + "\n")
        
        # =====================================================================
        # --- Task 3: An Insert Transaction Based on Data ---
        # =====================================================================
        print("--- Task 3: An Insert Transaction Based on Data ---")
        
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';")
        customer_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';")
        employee_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5;")
        cheapest_product_ids = [row[0] for row in cursor.fetchall()]
        
        try:
            insert_order_query = """
            INSERT INTO orders (customer_id, employee_id) 
            VALUES (?, ?) 
            RETURNING order_id;
            """
            cursor.execute(insert_order_query, (customer_id, employee_id))
            new_order_id = cursor.fetchone()[0]
            
            insert_item_query = """
            INSERT INTO line_items (order_id, product_id, quantity) 
            VALUES (?, ?, ?);
            """
            for prod_id in cheapest_product_ids:
                cursor.execute(insert_item_query, (new_order_id, prod_id, 10))
            
            conn.commit()
            print(f"Successfully committed Transaction for Order #{new_order_id}.")
            
        except Exception as transaction_error:
            conn.rollback()
            print(f"Transaction aborted and rolled back. Error: {transaction_error}")
            raise transaction_error

        verification_query = """
        SELECT 
            line_items.line_item_id,
            line_items.quantity,
            products.product_name
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
        WHERE line_items.order_id = ?;
        """
        cursor.execute(verification_query, (new_order_id,))
        verification_rows = cursor.fetchall()
        
        print(f"\nVerification Results for Order ID {new_order_id}:")
        print("-" * 50)
        for row in verification_rows:
            print(f"Line Item ID: {row[0]:<5} | Qty: {row[1]:<3} | Product: {row[2]}")

        # =====================================================================
        # --- Task 4: Aggregation with HAVING ---
        # =====================================================================
        print("\n" + "="*50 + "\n")
        print("--- Task 4: Aggregation with HAVING ---")
        
        query_task4 = """
        SELECT 
            employees.employee_id,
            employees.first_name,
            employees.last_name,
            COUNT(orders.order_id) AS order_count
        FROM employees
        JOIN orders ON employees.employee_id = orders.employee_id
        GROUP BY employees.employee_id
        HAVING order_count > 5;
        """
        cursor.execute(query_task4)
        rows_task4 = cursor.fetchall()
        
        for row in rows_task4:
            print(f"ID: {row[0]:<4} | Name: {row[1]} {row[2]:<15} | Orders Handled: {row[3]}")

        conn.close()
    except Exception as e:
        print(f"General Program Error: {e}")

if __name__ == "__main__":
    main()
