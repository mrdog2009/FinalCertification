from datetime import datetime

class BaseEntity():
    """Базовый абстрактный класс с id и датой создания."""

    def __init__(self, id=None, created_at=None):
        self._id = id
        self._created_at = created_at or datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass


class Client(BaseEntity):
    def __init__(self, id=None, name="", email="", phone="", created_at=None):
        super().__init__(id, created_at)
        self.name = name
        self.email = email
        self.phone = phone


    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data):
        created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else None
        return cls(id=data.get("id"), name=data.get("name", ""), email=data.get("email", ""),
                   phone=data.get("phone", ""), created_at=created_at)

    def __str__(self):
        return f"Client {self._id}: {self.name} ({self.email}, {self.phone})"


class Product(BaseEntity):
    def __init__(self, id=None, name="", price=0.0, created_at=None):
        super().__init__(id, created_at)
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "price": self.price,
            "created_at": self._created_at.isoformat(),
        }
    def get_name(self):
        return self.name

    @classmethod
    def from_dict(cls, data):
        created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else None
        return cls(id=data.get("id"), name=data.get("name", ""), price=float(data.get("price", 0.0)),
                   created_at=created_at)

    def __str__(self):
        return f"Product {self._id}: {self.name} ({self.price:.2f}) руб."


class OrderItem:
    """Связь заказа и товаров: продукт, количество"""

    def __init__(self, product: Product, quantity=1):
        self.product = product
        self.quantity = quantity

    def to_dict(self):
        return {
            "product_id": self.product.id,
            "quantity": self.quantity
        }

    def get_product_name(self):
        return ' ' + self.product.get_name()


class Order(BaseEntity):
    def __init__(self, id=None, client: Client = None, items=None, created_at=None):
        super().__init__(id, created_at)
        self.client = client
        self.items = items or []  # список OrderItem

    def total(self):
        return sum(item.product.price * item.quantity for item in self.items)

    def to_dict(self):
        return {
            "id": self._id,
            "client_id": self.client.id if self.client else None,
            "items": [item.to_dict() for item in self.items],
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data, clients_dict, products_dict):
        # clients_dict и products_dict — словари для связи id -> объект
        created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else None
        client = clients_dict.get(data.get("client_id"))
        items = []
        for item_data in data.get("items", []):
            product = products_dict.get(item_data["product_id"])
            if product:
                items.append(OrderItem(product, item_data["quantity"]))
        return cls(id=data.get("id"), client=client, items=items, created_at=created_at)

    def __str__(self):
        items_str = ", ".join([f"{item.product.name} x{item.quantity}" for item in self.items])
        return f"Order {self._id} for {self.client.name if self.client else 'Unknown'}: {items_str} Total: {self.total():.2f} руб."
