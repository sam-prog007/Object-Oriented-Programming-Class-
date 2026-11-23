"""E-commerce example from the course: domain functions + service layer."""

# ==============================================
# Domain layer (what unit tests target)
# ==============================================


def calculate_discount(price, discount_percent):
    """Return the discounted price."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return round(price * (1 - discount_percent / 100), 2)


def calculate_tax(price, tax_rate=0.20):
    """Return the tax amount."""
    return round(price * tax_rate, 2)


def calculate_total(prices, tax_rate=0.20):
    """Return the grand total including tax."""
    subtotal = sum(prices)
    tax = calculate_tax(subtotal, tax_rate)
    return round(subtotal + tax, 2)


# ==============================================
# Service / repository layer (integration tests)
# ==============================================


class ProductRepository:
    """Simulates a database of products."""

    def __init__(self):
        self._products = {
            "SHIRT": {"name": "T-Shirt", "price": 25.00, "stock": 50},
            "MUG": {"name": "Coffee Mug", "price": 12.00, "stock": 100},
            "HAT": {"name": "Cap", "price": 18.00, "stock": 30},
        }

    def get_product(self, sku):
        return self._products.get(sku)

    def update_stock(self, sku, quantity):
        product = self._products.get(sku)
        if product and product["stock"] >= quantity:
            product["stock"] -= quantity
            return True
        return False


class OrderService:
    """Business logic that coordinates the repository and the calculations."""

    def __init__(self, repo):
        self.repo = repo

    def place_order(self, sku, quantity):
        product = self.repo.get_product(sku)
        if product is None:
            return {"success": False, "error": "Product not found"}
        if product["stock"] < quantity:
            return {"success": False, "error": "Not enough stock"}
        total = calculate_total([product["price"] * quantity])
        self.repo.update_stock(sku, quantity)
        return {
            "success": True,
            "item": product["name"],
            "quantity": quantity,
            "total": total,
        }
