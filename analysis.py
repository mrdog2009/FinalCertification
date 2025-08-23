import matplotlib.pyplot as plt
from dateutil.parser import parse
import networkx as nx
import pandas as pd
import seaborn as sns

from models import OrderItem, Product


def sales_over_time(orders):
    """
    Построение графика продаж по дням на основе списка заказов.

    Args:
        orders: Список - список продаж.

    Returns:
        визуализация графика
    """
    sales_by_date = {}
    for order in orders:
        date = parse(order.created_at).date()

        #date = order.created_at
        sales_by_date.setdefault(date, 0.0)
        sales_by_date[date] += order.total()

    dates = sorted(sales_by_date.keys())
    sales = [sales_by_date[d] for d in dates]

    plt.figure(figsize=(10,5))
    plt.plot(dates, sales, marker='o')
    #plt.plot([10,20,30,40,50], [1,2,3,4,5], marker='o')
    plt.title("Динамика продаж по дням")
    plt.xlabel("Дата")
    plt.ylabel("Сумма продаж")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def top5_products(df):
    """
    Построение гистограммы 5 самых продаваемых товаров на основе списка заказов.

    Args:
        df (pd.DataFrame): DataFrame.

    Returns:
        визуализация гистограммы
    """

    if not df.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='name', y='order_count', data=df)
        plt.title('Топ5 клиентов по количеству заказов')
        plt.xlabel('Клиент')
        plt.ylabel('Количество заказов')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("Нет данных для визуализации.")


def graph_relationship(orders):
    """
    Построение графа на основе списка заказов.
    Узлы графа - клиенты и продукты.
    Ребра соединяют клиентов с продуктами, которые они заказывали.

    Args:
        orders: Список - список продаж.

    Returns:
        визуализация графа.
    """

    # выделяем всех клиентов из orders
    clients = set()
    products = set()
    graph = nx.Graph()

    for order in orders:
        client = order.client
        clients.add(client.name)
        graph.add_node(client.name, type="client")

        for product in order.items:
            pr =product.get_product_name()
            products.add(pr)
            graph.add_node(pr, type="product")
            graph.add_edge(client.name, pr)

    pos = {}
    y_offset = 0  # Смещение по вертикали для первого узла
    y_spacing = 1.0 # Вертикальное расстояние между узлами
    num_customers = len(clients)
    num_products = len(products)

    # помещаем продукты слева и центрируем по вертикали
    for i, product in enumerate(products):
        pos[product] = (-1, (num_products-1) * y_spacing / 2 - i*y_spacing - y_offset)

    # клиенты - справа и центрируем
    for i, customer in enumerate(clients):
        pos[customer] = (1, (num_customers-1) * y_spacing / 2 - i*y_spacing - y_offset)

    plt.figure(figsize=(8, 6))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=1500,
        font_size=10,
        width=0.5,
        edgecolors="gray",
    )
    plt.show()