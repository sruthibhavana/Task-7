import sqlite3
import matplotlib.pyplot as plt
import csv

DB_NAME = 'sales_data.db'
CSV_FILE = 'revenue_summary.csv'

def create_connection(db_name):
    return sqlite3.connect(db_name)

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            product TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')

def insert_sample_data(cursor):
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("2025-05-05", "Headphones", 4, 150.00),
            ("2025-05-05", "Monitor", 2, 300.00),
            ("2025-05-06", "Keyboard", 6, 90.00),
            ("2025-05-06", "Mouse", 8, 40.00),
            ("2025-05-07", "Monitor", 1, 300.00),
            ("2025-05-07", "Headphones", 3, 150.00),
        ]
        cursor.executemany(
            'INSERT INTO sales (date, product, quantity, price) VALUES (?, ?, ?, ?)',
            sample_data
        )

def fetch_revenue_by_product(cursor):
    cursor.execute('''
        SELECT product, SUM(quantity * price) AS revenue
        FROM sales
        GROUP BY product
    ''')
    return cursor.fetchall()

def display_results(results):
    print("Total Revenue by Product:")
    for product, revenue in results:
        print(f"{product}: ${revenue:,.2f}")

def save_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Product", "Revenue"])
        for row in results:
            writer.writerow(row)
    print(f"\nRevenue data saved to '{filename}'")

def plot_revenue(results):
    products = [row[0] for row in results]
    revenues = [row[1] for row in results]

    plt.figure(figsize=(6, 4))
    plt.bar(products, revenues, color='skyblue')
    plt.title('Total Revenue by Product')
    plt.xlabel("Product")
    plt.ylabel("Revenue ($)")
    plt.tight_layout()
    plt.show()

def main():
    try:
        with create_connection(DB_NAME) as conn:
            cursor = conn.cursor()
            create_table(cursor)
            insert_sample_data(cursor)
            conn.commit()
            results = fetch_revenue_by_product(cursor)
            display_results(results)
            save_to_csv(results, CSV_FILE)
            plot_revenue(results)
    except sqlite3.Error as e:
        print("Database error:", e)

if __name__ == "__main__":
    main()
