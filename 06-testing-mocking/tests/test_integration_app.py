"""Integration tests: OrderService + ProductRepository + calculation functions together."""


class TestIntegrationOrderService:
    def test_integration_successful_order(self, order_service):
        result = order_service.place_order("SHIRT", 2)
        assert result == {"success": True, "item": "T-Shirt", "quantity": 2, "total": 60.0}

    def test_integration_stock_is_reduced_after_order(self, order_service):
        order_service.place_order("MUG", 3)
        assert order_service.repo.get_product("MUG")["stock"] == 97

    def test_integration_order_unknown_product(self, order_service):
        result = order_service.place_order("PANTS", 1)
        assert result == {"success": False, "error": "Product not found"}

    def test_integration_order_exceeds_stock(self, order_service):
        result = order_service.place_order("HAT", 999)
        assert result == {"success": False, "error": "Not enough stock"}

    def test_integration_failed_order_keeps_stock(self, order_service):
        order_service.place_order("HAT", 999)
        assert order_service.repo.get_product("HAT")["stock"] == 30

    def test_integration_multiple_orders_deplete_stock(self, order_service):
        order_service.place_order("HAT", 10)
        order_service.place_order("HAT", 15)
        assert order_service.repo.get_product("HAT")["stock"] == 5

    def test_integration_service_with_mocked_repository(self, mocker):
        """The repository is mocked: we check the service talks to it correctly."""
        from src.app import OrderService
        fake_repo = mocker.Mock()
        fake_repo.get_product.return_value = {"name": "Mock", "price": 10.0, "stock": 5}
        result = OrderService(fake_repo).place_order("ANY", 2)
        assert result["total"] == 24.0
        fake_repo.update_stock.assert_called_once_with("ANY", 2)
