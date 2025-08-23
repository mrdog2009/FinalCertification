import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db import DB
from models import Client, Product, Order, OrderItem
import analysis
import re

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Менеджер Интернет-магазина")
        self.geometry("900x700")

        self.db = DB()

        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        self.tab_clients = ttk.Frame(tab_control)
        self.tab_products = ttk.Frame(tab_control)
        self.tab_orders = ttk.Frame(tab_control)
        self.tab_analysis = ttk.Frame(tab_control)

        tab_control.add(self.tab_clients, text="Клиенты")
        tab_control.add(self.tab_products, text="Товары")
        tab_control.add(self.tab_orders, text="Заказы")
        tab_control.add(self.tab_analysis, text="Анализ")
        tab_control.pack(expand=1, fill='both')

        self.create_clients_tab()
        self.create_products_tab()
        self.create_orders_tab()
        self.create_analysis_tab()

    # ------ КЛИЕНТЫ --------
    def create_clients_tab(self):
        frm = self.tab_clients

        # Форма добавления клиента
        frm_add = ttk.LabelFrame(frm, text="Добавить клиента")
        frm_add.pack(fill='x', padx=5, pady=5)

        ttk.Label(frm_add, text="Имя:").grid(row=0, column=0)
        self.client_name_var = tk.StringVar()
        ttk.Entry(frm_add, textvariable=self.client_name_var).grid(row=0, column=1)

        ttk.Label(frm_add, text="Email:").grid(row=1, column=0)
        self.client_email_var = tk.StringVar()
        ttk.Entry(frm_add, textvariable=self.client_email_var).grid(row=1, column=1)

        ttk.Label(frm_add, text="Телефон:").grid(row=2, column=0)
        self.client_phone_var = tk.StringVar()
        ttk.Entry(frm_add, textvariable=self.client_phone_var).grid(row=2, column=1)

        ttk.Button(frm_add, text="Добавить", command=self.add_client).grid(row=3, column=0, columnspan=2, pady=5)

        # Список клиентов
        frm_list = ttk.LabelFrame(frm, text="Клиенты")
        frm_list.pack(fill='both', expand=1, padx=5, pady=5)

        columns = ("id", "name", "email", "phone")
        self.client_tree = ttk.Treeview(frm_list, columns=columns, show="headings")
        for col in columns:
            self.client_tree.heading(col, text=col.title())
            self.client_tree.column(col, anchor=tk.W, width=100)
        self.client_tree.pack(fill='both', expand=1)

        # Кнопки импорта/экспорта
        frm_buttons = ttk.Frame(frm)
        frm_buttons.pack(fill='x', padx=5, pady=5)
        ttk.Button(frm_buttons, text="Экспорт CSV", command=self.export_clients_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_buttons, text="Импорт CSV", command=self.import_clients_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_buttons, text="Экспорт JSON", command=self.export_clients_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_buttons, text="Импорт JSON", command=self.import_clients_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_buttons, text="Обновить список", command=self.load_clients).pack(side=tk.RIGHT)

        self.load_clients()


    def add_client(self):
        def validate_email(email):
            pattern = r"[a-zA-Z0-9а-яА-Я._%+-]+@[a-zA-Z0-9а-яА-Я.-]+\.[a-zA-Zа-яА-Я]{2,}"
            if not re.match(pattern, email):
                return False
            return True

        def validate_phone(phone):
            pattern = r"^\+[0-9]{1,11}"
            if not re.match(pattern, phone):
                return False
            return True

        name = self.client_name_var.get()
        email = self.client_email_var.get()
        phone = self.client_phone_var.get()
        if not name:
            messagebox.showerror("Ошибка", "Имя клиента обязательно")
            return
        if not validate_email(email):
            messagebox.showerror("Ошибка", "Не верный email")
            return
        if not validate_phone(phone):
            messagebox.showerror("Ошибка", "Не верный номер телефона")
            return
        client = Client(name=name, email=email, phone=phone)
        self.db.add_client(client)
        messagebox.showinfo("Успех", "Клиент добавлен")
        self.client_name_var.set("")
        self.client_email_var.set("")
        self.client_phone_var.set("")
        self.load_clients()
        self.load_clients_for_order()  # обновление списка клиентов в ComboBox в таб Заказы при добавлении нового клиента


    def load_clients(self):
        for row in self.client_tree.get_children():
            self.client_tree.delete(row)
        clients = self.db.get_clients()
        for c in clients:
            self.client_tree.insert("", "end", values=(c.id, c.name, c.email, c.phone))

    def export_clients_csv(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if f:
            self.db.export_clients_csv(f)
            messagebox.showinfo("Экспорт", "Клиенты экспортированы в CSV")

    def import_clients_csv(self):
        f = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if f:
            self.db.import_clients_csv(f)
            messagebox.showinfo("Импорт", "Клиенты импортированы из CSV")
            self.load_clients()

    def export_clients_json(self):
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if f:
            self.db.export_clients_json(f)
            messagebox.showinfo("Экспорт", "Клиенты экспортированы в JSON")

    def import_clients_json(self):
        f = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if f:
            self.db.import_clients_json(f)
            messagebox.showinfo("Импорт", "Клиенты импортированы из JSON")
            self.load_clients()

    # ----------------- ТОВАРЫ -------------------
    def create_products_tab(self):
        frm = self.tab_products

        frm_add = ttk.LabelFrame(frm, text="Добавить продукт")
        frm_add.pack(fill='x', padx=5, pady=5)

        ttk.Label(frm_add, text="Название:").grid(row=0, column=0)
        self.product_name_var = tk.StringVar()
        ttk.Entry(frm_add, textvariable=self.product_name_var).grid(row=0, column=1)

        ttk.Label(frm_add, text="Цена:").grid(row=1, column=0)
        self.product_price_var = tk.StringVar()
        ttk.Entry(frm_add, textvariable=self.product_price_var).grid(row=1, column=1)

        ttk.Button(frm_add, text="Добавить", command=self.add_product).grid(row=2, column=0, columnspan=2, pady=5)

        frm_list = ttk.LabelFrame(frm, text="Товары")
        frm_list.pack(fill='both', expand=1, padx=5, pady=5)

        columns = ("id", "name", "price")
        self.product_tree = ttk.Treeview(frm_list, columns=columns, show="headings")
        for col in columns:
            self.product_tree.heading(col, text=col.title())
            self.product_tree.column(col, anchor=tk.W, width=100)
        self.product_tree.pack(fill='both', expand=1)

        ttk.Button(frm, text="Обновить список", command=self.load_products).pack(side=tk.RIGHT)
        self.load_products()

    def add_product(self):
        name = self.product_name_var.get()
        price_str = self.product_price_var.get()
        try:
            price = float(price_str)
        except:
            messagebox.showerror("Ошибка", "Цена должна быть числом")
            return
        if not name:
            messagebox.showerror("Ошибка", "Название продукта обязательно")
            return
        product = Product(name=name, price=price)
        self.db.add_product(product)
        messagebox.showinfo("Успех", "Продукт добавлен")
        self.product_name_var.set("")
        self.product_price_var.set("")
        self.load_products()
        self.load_products_for_order() #обновление списка товаров в ListBox в табе Заказов при создании нового товара


    def load_products(self):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)
        products = self.db.get_products()
        for p in products:
            self.product_tree.insert("", "end", values=(p.id, p.name, f"{p.price:.2f}"))

    # ----------------- ЗАКАЗЫ -------------------
    def create_orders_tab(self):
        frm = self.tab_orders

        frm_add = ttk.LabelFrame(frm, text="Создать заказ")
        frm_add.pack(fill='x', padx=5, pady=5)

        ttk.Label(frm_add, text="Клиент:").grid(row=0, column=0)
        self.order_client_var = tk.StringVar()
        self.combobox_clients = ttk.Combobox(frm_add, textvariable=self.order_client_var)
        self.combobox_clients.grid(row=0, column=1)

        ttk.Label(frm_add, text="Товары:").grid(row=1, column=0)
        self.products_listbox = tk.Listbox(frm_add, selectmode=tk.MULTIPLE, height=10)
        self.products_listbox.grid(row=1, column=1)

        ttk.Label(frm_add, text="Кол-во для выбранных товаров (через запятую):").grid(row=2, column=0)
        self.order_quantities_var = tk.StringVar()
        ttk.Entry(frm_add, textvariable=self.order_quantities_var).grid(row=2, column=1)

        ttk.Button(frm_add, text="Создать заказ", command=self.add_order).grid(row=3, column=0, columnspan=2, pady=5)

        frm_list = ttk.LabelFrame(frm, text="Заказы")
        frm_list.pack(fill='both', expand=1, padx=5, pady=5)

        columns = ("id", "client", "items", "total", "created_at")
        self.order_tree = ttk.Treeview(frm_list, columns=columns, show="headings")
        for col in columns:
            self.order_tree.heading(col, text=col.title())
            if col == "items":
                self.order_tree.column(col, width=300)
            else:
                self.order_tree.column(col, width=100)
        self.order_tree.pack(fill='both', expand=1)

        frm_filter = ttk.Frame(frm)
        frm_filter.pack(fill='x', padx=5, pady=5)

        ttk.Label(frm_filter, text="Фильтр по имени клиента:").pack(side=tk.LEFT)
        self.filter_client_name_var = tk.StringVar()
        ttk.Entry(frm_filter, textvariable=self.filter_client_name_var).pack(side=tk.LEFT)
        ttk.Button(frm_filter, text="Применить фильтр", command=self.load_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_filter, text="Сбросить фильтр", command=self.reset_filter_orders).pack(side=tk.LEFT)
        ttk.Button(frm, text="Обновить список", command=self.load_orders).pack(side=tk.RIGHT)

        self.load_orders()
        self.load_clients_for_order()
        self.load_products_for_order()

    def load_clients_for_order(self):
        clients = self.db.get_clients()
        self.clients_map = {str(c.id): c for c in clients}
        self.combobox_clients["values"] = [f"{c.id} - {c.name}" for c in clients]

    def load_products_for_order(self):
        products = self.db.get_products()
        self.products_map = {p.id: p for p in products}
        self.products_listbox.delete(0, tk.END)
        for p in products:
            self.products_listbox.insert(tk.END, f"{p.id} - {p.name} ({p.price:.2f} руб.)")

    def add_order(self):
        selected_client = self.order_client_var.get()
        if not selected_client:
            messagebox.showerror("Ошибка", "Выберите клиента")
            return
        client_id = selected_client.split(" - ")[0]
        client = None
        for c in self.db.get_clients():
            if str(c.id) == client_id:
                client = c
                break
        if not client:
            messagebox.showerror("Ошибка", "Клиент не найден")
            return

        selected_indices = list(self.products_listbox.curselection())
        if not selected_indices:
            messagebox.showerror("Ошибка", "Выберите товары")
            return

        quantities_text = self.order_quantities_var.get()
        quantities = []
        if quantities_text:
            quantities = [q.strip() for q in quantities_text.split(",")]
        if quantities and len(quantities) != len(selected_indices):
            messagebox.showerror("Ошибка", "Количество чисел не совпадает с количеством выбранных товаров")
            return
        try:
            quantities = list(map(int, quantities)) if quantities else [1] * len(selected_indices)
        except:
            messagebox.showerror("Ошибка", "Кол-во товаров должно быть числом")
            return

        items = []
        for idx, q in zip(selected_indices, quantities):
            product_str = self.products_listbox.get(idx)
            product_id = int(product_str.split(" - ")[0])
            product = self.products_map.get(product_id)
            if product and q > 0:
                items.append(OrderItem(product, q))

        if not items:
            messagebox.showerror("Ошибка", "Количество товаров должно быть больше нуля")
            return

        order = Order(client=client, items=items)
        self.db.add_order(order)
        messagebox.showinfo("Успех", f"Заказ №{order.id} создан")
        self.order_quantities_var.set("")
        self.load_orders()

    def load_orders(self):
         for row in self.order_tree.get_children():
             self.order_tree.delete(row)
         filter_name = self.filter_client_name_var.get()
         filters = {"client_name": filter_name} if filter_name else None
         orders = self.db.get_orders(filters=filters, order_by="created_at DESC")
         print(*orders)
         for o in orders:
             items_str = ", ".join([f"{item.product.name} x{item.quantity}" for item in o.items])
             self.order_tree.insert("", "end", values=(o.id, o.client.name if o.client else "unknown", items_str, f"{o.total():.2f} руб.", o.created_at))

    def reset_filter_orders(self):
        self.filter_client_name_var.set("")
        self.load_orders()

    # ------------- АНАЛИЗ --------------
    def create_analysis_tab(self):
        frm = self.tab_analysis
        ttk.Button(frm, text="Динамика продаж по дням", command=self.show_sales_over_time).pack(pady=10)
        ttk.Button(frm, text="Топ товаров", command=self.show_top_products).pack(pady=10)
        ttk.Button(frm, text="Граф связей клиентов", command=self.show_graph_relationship).pack(pady=10)

    def show_sales_over_time(self):
        orders = self.db.get_orders()
        analysis.sales_over_time(orders)

    def show_top_products(self):
        df = self.db.get_top5_products()
        analysis.top5_products(df)

    def show_graph_relationship(self):
        orders = self.db.get_orders()
        analysis.graph_relationship(orders)