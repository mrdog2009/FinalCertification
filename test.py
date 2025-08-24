import unittest
from models import Client, Product, Order, OrderItem
from gui import App

class TestClient(unittest.TestCase):
    def test_client_creation(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google.com",
            phone="+7(123)456-7890",
            created_at="2025-08-01",
        )
        self.assertEqual(client.name, "Макаров Макар")
        self.assertEqual(client.email, "MMakarov@google.com")

    def test_invalid1_email(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google",
            phone="+7(123)456-7890",
            created_at="2025-08-01",
        )

        self.assertEqual(App().validate_email(client.email), False)

    def test_invalid2_email(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov_google.com",
            phone="+7(123)456-7890",
            created_at="2025-08-01",
        )
        self.assertEqual(App().validate_email(client.email), False)

    def test_correct_email(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google.com",
            phone="+7(123)456-7890",
            created_at="2025-08-01",
        )
        self.assertEqual(App().validate_email(client.email), True)

    def test_invalid1_phone(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google.com",
            phone="8(123)456-7890",
            created_at="2025-08-01",
        )
        self.assertEqual(App().validate_phone(client.phone), False)

    def test_invalid2_phone(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google.com",
            phone="+",
            created_at="2025-08-01",
        )
        self.assertEqual(App().validate_phone(client.phone), False)

    def test_correct_phone(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google.com",
            phone="+7(123)456-7890",
            created_at="2025-08-01",
        )
        self.assertEqual(App().validate_phone(client.phone), True)

class TestProduct(unittest.TestCase):
    def test_product_creation(self):
        product = Product(
            id=1,
            name="Рыба",
            price=1200.00,
            created_at="2025-08-01",
        )
        self.assertEqual(product.name, "Рыба")
        self.assertEqual(product.price, 1200.00)

class TestOrder(unittest.TestCase):
    def test_order_calculate_total(self):
        client = Client(
            id=1,
            name="Макаров Макар",
            email="MMakarov@google.com",
            phone="+7(123)456-7890",
            created_at="2025-08-01",
        )
        product = Product(
            id=1,
            name="Рыба",
            price=1200.00,
            created_at="2025-08-01",
        )
        orderitem = OrderItem(
            product = product,
            quantity = 3,
        )
        items = []
        items.append(orderitem)
        order = Order(
            id=1,
            client=client,
            items=items,
            created_at="2025-08-01"
        )
        self.assertEqual(order.total(), 3600)


if __name__ == '__main__':
    unittest.main()