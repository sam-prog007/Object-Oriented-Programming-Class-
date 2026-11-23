import json

import pytest

from adapter_report import LegacyReportAdapter, LegacyReportGenerator, ReportGeneratorInterface
from decorator_order import (
    BaseOrder,
    DiscountDecorator,
    ExpressShippingDecorator,
    GiftWrapDecorator,
    InsuranceDecorator,
    PremiumMemberDecorator,
)


# ------------------------------------------------------------------ Adapter ---
class TestAdapter:
    @pytest.fixture
    def adapter(self):
        return LegacyReportAdapter(LegacyReportGenerator())

    def test_adapter_implements_interface(self, adapter):
        assert isinstance(adapter, ReportGeneratorInterface)

    def test_output_is_valid_json_with_types(self, adapter):
        data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
        assert json.loads(adapter.generate(data)) == data

    def test_adapter_really_uses_legacy_xml(self, mocker):
        legacy = LegacyReportGenerator()
        spy = mocker.spy(legacy, "generate_report")
        LegacyReportAdapter(legacy).generate({"a": 1})
        spy.assert_called_once_with({"a": 1})

    def test_text_values_stay_text(self, adapter):
        assert json.loads(adapter.generate({"region": "EMEA"})) == {"region": "EMEA"}


# ---------------------------------------------------------------- Decorator ---
class TestDecorator:
    def test_base_order(self):
        assert BaseOrder(100).get_cost() == 100

    def test_each_option(self):
        assert ExpressShippingDecorator(BaseOrder(100)).get_cost() == 115
        assert InsuranceDecorator(BaseOrder(100)).get_cost() == 105
        assert GiftWrapDecorator(BaseOrder(100)).get_cost() == 105
        assert DiscountDecorator(BaseOrder(100), percent=15).get_cost() == 85
        assert PremiumMemberDecorator(BaseOrder(100)).get_cost() == 90

    def test_full_stack_matches_legacy_total(self):
        order = BaseOrder(100.0)
        order = ExpressShippingDecorator(order)
        order = InsuranceDecorator(order)
        order = GiftWrapDecorator(order)
        order = DiscountDecorator(order, percent=15)
        order = PremiumMemberDecorator(order)
        assert order.get_cost() == pytest.approx(95.625)   # same as the original spaghetti code

    def test_insurance_is_on_base_price(self):
        order = InsuranceDecorator(ExpressShippingDecorator(BaseOrder(100)))
        assert order.get_cost() == pytest.approx(120)       # 100 + 15 + 5% of 100

    def test_description_lists_every_option(self):
        order = GiftWrapDecorator(ExpressShippingDecorator(BaseOrder(50)))
        text = order.get_description()
        assert "Base price" in text and "Express shipping" in text and "Gift wrap" in text

    def test_decorators_can_repeat(self):
        assert GiftWrapDecorator(GiftWrapDecorator(BaseOrder(10))).get_cost() == 20

    def test_invalid_discount(self):
        with pytest.raises(ValueError):
            DiscountDecorator(BaseOrder(10), percent=150)
