"""Unit tests: ONE function in isolation, fast, no outside world."""

import pytest

from src.app import ProductRepository, calculate_discount, calculate_tax, calculate_total


class TestUnitDiscount:
    def test_unit_10_percent_off(self):
        assert calculate_discount(100, 10) == 90.0

    def test_unit_full_price_when_zero_discount(self):
        assert calculate_discount(50, 0) == 50.0

    def test_unit_free_when_100_percent_discount(self):
        assert calculate_discount(75, 100) == 0.0

    def test_unit_handles_decimals(self):
        assert calculate_discount(19.99, 15) == 16.99

    def test_unit_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10, 20)

    @pytest.mark.parametrize("bad_discount", [-1, 101, 150])
    def test_unit_out_of_range_discounts_rejected(self, bad_discount):
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100, bad_discount)


class TestUnitTax:
    def test_unit_default_20_percent_tax(self):
        assert calculate_tax(100) == 20.0

    def test_unit_custom_tax_rate(self):
        assert calculate_tax(100, 0.10) == 10.0

    def test_unit_zero_price_zero_tax(self):
        assert calculate_tax(0) == 0.0


class TestUnitTotal:
    def test_unit_single_item_total(self):
        assert calculate_total([50.0]) == 60.0            # 50 + 20% tax

    def test_unit_multiple_items_total(self):
        assert calculate_total([10.0, 20.0, 30.0]) == 72.0

    def test_unit_empty_cart(self):
        assert calculate_total([]) == 0.0

    def test_unit_custom_tax_rate_total(self):
        # Arrange
        prices = [100.0]
        # Act
        total = calculate_total(prices, tax_rate=0.05)
        # Assert
        assert total == 105.0


class TestUnitRepository:
    def test_unit_get_existing_product(self, repo):
        assert repo.get_product("MUG")["price"] == 12.00

    def test_unit_get_unknown_product(self, repo):
        assert repo.get_product("NOPE") is None

    def test_unit_update_stock(self):
        r = ProductRepository()
        assert r.update_stock("HAT", 5) is True
        assert r.get_product("HAT")["stock"] == 25

    def test_unit_update_stock_refused_when_too_many(self, repo):
        assert repo.update_stock("HAT", 999) is False
        assert repo.update_stock("NOPE", 1) is False
