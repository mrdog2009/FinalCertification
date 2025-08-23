import sqlite3
from models import Client, Product, Order, OrderItem

class DB:
    def __init__(self, db_path="shop.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            created_at DATETIME
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            created_at DATETIME
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            created_at DATETIME,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )''')

        self.conn.commit()

    # --- Клиенты ---
    def add_client(self, client: Client):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO clients (name,email,phone,created_at) VALUES (?,?,?,?)",
                    (client.name, client.email, client.phone, client.created_at.isoformat()))
        self.conn.commit()
        client._id = cur.lastrowid
        return client

    def get_clients(self, filters=None, order_by=None):
        cur = self.conn.cursor()
        query = "SELECT * FROM clients"
        params = []
        if filters:
            clauses = []
            for k,v in filters.items():
                clauses.append(f"{k} LIKE ?")
                params.append(f"%{v}%")
            query += " WHERE " + " AND ".join(clauses)
        if order_by:
            query += f" ORDER BY {order_by}"
        cur.execute(query, params)
        rows = cur.fetchall()
        clients = [Client(id=row["id"], name=row["name"], email=row["email"],
                          phone=row["phone"],
                          created_at = row["created_at"]) for row in rows]
        return clients

    # --- Продукты ---
    def add_product(self, product: Product):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO products (name, price, created_at) VALUES (?, ?, ?)",
                    (product.name, product.price, product.created_at.isoformat()))
        self.conn.commit()
        product._id = cur.lastrowid
        return product

    def get_products(self, filters=None):
        cur = self.conn.cursor()
        query = "SELECT * FROM products"
        params = []
        if filters:
            clauses = []
            for k,v in filters.items():
                clauses.append(f"{k} LIKE ?")
                params.append(f"%{v}%")
            query += " WHERE " + " AND ".join(clauses)
        cur.execute(query, params)
        rows = cur.fetchall()
        products = [Product(id=row["id"], name=row["name"], price=row["price"],
                            created_at = row["created_at"]) for row in rows]
        return products

    # --- Заказы ---
    def add_order(self, order: Order):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO orders (client_id, created_at) VALUES (?, ?)",
                    (order.client.id if order.client else None, order.created_at.isoformat()))
        order_id = cur.lastrowid

        for item in order.items:
            cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                        (order_id, item.product.id, item.quantity))
        self.conn.commit()
        order._id = order_id
        return order

    def get_orders(self, filters=None, order_by=None):
        # filters: {'client_name': 'John'}
        cur = self.conn.cursor()

        query = """SELECT o.id, o.client_id, o.created_at, c.name as client_name
                   FROM orders o
                   LEFT JOIN clients c ON o.client_id = c.id"""
        params = []

        if filters:
            clauses = []
            if "client_name" in filters and filters["client_name"]:
                clauses.append("c.name LIKE ?")
                params.append(f"%{filters['client_name']}%")
            if "date_from" in filters and filters["date_from"]:
                clauses.append("o.created_at >= ?")
                params.append(filters["date_from"])
            if "date_to" in filters and filters["date_to"]:
                clauses.append("o.created_at <= ?")
                params.append(filters["date_to"])
            if clauses:
                query += " WHERE " + " AND ".join(clauses)


        cur.execute(query, params)
        order_rows = cur.fetchall()

        # Получим клиентов и продукты для связи
        client_ids = list(set(row["client_id"] for row in order_rows if row["client_id"] is not None))
        clients = {}
        if client_ids:
            q = "SELECT * FROM clients WHERE id IN ({})".format(",".join("?"*len(client_ids)))
            cur.execute(q, client_ids)
            for r in cur:
                clients[r["id"]] = Client(id=r["id"], name=r["name"], email=r["email"], phone=r["phone"], created_at=r["created_at"])

        product_rows = cur.execute("SELECT * FROM products").fetchall()
        products = {row["id"]: Product(id=row["id"], name=row["name"], price=row["price"], created_at=row["created_at"]) for row in product_rows}

        orders = []
        for order_row in order_rows:
            order_id = order_row["id"]
            cur.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,))
            items_rows = cur.fetchall()
            items = []
            for irow in items_rows:
                p = products.get(irow["product_id"])
                if p:
                    items.append(OrderItem(p, irow["quantity"]))
            o = Order(id=order_id, client=clients.get(order_row["client_id"]), items=items, created_at=order_row["created_at"])
            orders.append(o)

        return orders

    # --- Импорт / экспорт (CSV/JSON) ---
    def export_clients_csv(self, filepath):
        import csv
        clients = self.get_clients()
        with open(filepath, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "email", "phone", "created_at"])
            for c in clients:
                writer.writerow([c.id, c.name, c.email, c.phone, c.created_at])

    def import_clients_csv(self, filepath):
        import csv
        with open(filepath, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                c = Client(name=row["name"], email=row["email"], phone=row["phone"])
                self.add_client(c)

    def export_clients_json(self, filepath):
        import json
        clients = self.get_clients()
        data = [c.to_dict() for c in clients]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def import_clients_json(self, filepath):
        import json
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                c = Client.from_dict(item)
                self.add_client(c)

    def close(self):
        self.conn.close()


    def get_top5_products(self):
        import pandas as pd
        query = """SELECT c.name, COUNT(o.id) AS order_count
                    FROM clients c
                    LEFT JOIN orders o ON c.id = o.client_id
                    GROUP BY c.id
                    ORDER BY order_count DESC
                    LIMIT 5"""
        df = pd.read_sql_query(query, con=self.conn)
        return df