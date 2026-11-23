"""Decorator: refactor the order pricing system.

Before: calculate_total() with 5 boolean flags and one if per option.
After: each option is a wrapper object that adds its cost and description,
and wrappers can be stacked in any combination and order.
"""

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    """Common interface for the base order and every decorator."""

    @abstractmethod
    def get_cost(self) -> float:
        ...

    @abstractmethod
    def get_description(self) -> str:
        ...

    @abstractmethod
    def get_base_price(self) -> float:
        """The original price, before any option (insurance is computed on it)."""


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base price: {self.base_price:.2f}€"

    def get_base_price(self) -> float:
        return self.base_price


class OrderDecorator(OrderComponent):
    """Base decorator: holds the wrapped order and delegates to it by default.

    The wrapped object is stored as _order (one underscore, "protected") so
    subclasses can use it, as the slides recommend.
    """

    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()

    def get_base_price(self) -> float:
        return self._order.get_base_price()


class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00

    def get_cost(self) -> float:
        return self._order.get_cost() + self.COST

    def get_description(self) -> str:
        return self._order.get_description() + f"\nExpress shipping: +{self.COST:.2f}€"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05   # 5 % of the base price, as in the original code

    def _insurance(self) -> float:
        return self.get_base_price() * self.RATE

    def get_cost(self) -> float:
        return self._order.get_cost() + self._insurance()

    def get_description(self) -> str:
        return self._order.get_description() + f"\nInsurance (5%): +{self._insurance():.2f}€"


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def get_cost(self) -> float:
        return self._order.get_cost() + self.COST

    def get_description(self) -> str:
        return self._order.get_description() + f"\nGift wrap: +{self.COST:.2f}€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        super().__init__(order)
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        self.percent = percent

    def _discount(self) -> float:
        return self._order.get_cost() * self.percent / 100

    def get_cost(self) -> float:
        return self._order.get_cost() - self._discount()

    def get_description(self) -> str:
        return self._order.get_description() + f"\nDiscount ({self.percent}%): -{self._discount():.2f}€"


class PremiumMemberDecorator(DiscountDecorator):
    """A premium member is just a fixed 10 % discount: reuse DiscountDecorator."""

    def __init__(self, order: OrderComponent):
        super().__init__(order, percent=10)

    def get_description(self) -> str:
        return self._order.get_description() + f"\nPremium member (10%): -{self._discount():.2f}€"


if __name__ == "__main__":
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"TOTAL: {simple.get_cost():.2f}€\n---")

    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"TOTAL: {order.get_cost():.2f}€")
