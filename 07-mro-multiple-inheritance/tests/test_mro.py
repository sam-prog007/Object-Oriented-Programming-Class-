import pytest

from diamond import A, B, C, D, E, G, mro_names
from mixins import Catalog, JsonExporter, Product, SmartProduct
from super_chain import Child


class TestDiamond:
    def test_left_parent_wins(self):
        assert D().who_am_i() == "Class B"

    def test_parent_order_matters(self):
        assert E().who_am_i() == "Class C"

    def test_trap_c_before_a(self):
        assert G().who_am_i() == "Class C"     # not "Class A"

    def test_mro_order(self):
        assert mro_names(D) == ["D", "B", "C", "A", "object"]
        assert mro_names(E) == ["E", "C", "B", "A", "object"]

    def test_mro_types(self):
        assert isinstance(D.__mro__, tuple) and isinstance(D.mro(), list)

    def test_inconsistent_mro_is_refused(self):
        with pytest.raises(TypeError, match="consistent method resolution"):
            type("Bad", (A, B), {})            # A cannot come before its child B


class TestSuper:
    def test_each_class_runs_once_in_mro_order(self):
        log = []
        Child().greet(log)
        assert log == ["Child", "Left", "Right", "Base"]


class TestMixins:
    def test_mixin_adds_json(self):
        assert SmartProduct("Mug", 12.0).to_json() == '{"name": "Mug", "price": 12.0}'

    def test_mixin_adds_repr(self):
        assert repr(SmartProduct("Mug", 12.0)) == "SmartProduct(name='Mug', price=12.0)"

    def test_real_parent_is_last_before_object(self):
        assert SmartProduct.__mro__[-2] is Product

    def test_composition_alternative(self):
        catalog = Catalog(JsonExporter())
        catalog.add(Product("Cap", 18.0))
        assert catalog.export_all() == ['{"name": "Cap", "price": 18.0}']
