"""Mixins (the table of contents: "Mixins and composition patterns").

A mixin is a small class that adds ONE reusable ability. It is not meant to be
used alone. This is the one place where multiple inheritance is reasonable:
the "real" parent comes last, the mixins in front of it.
"""

import json


class JsonMixin:
    """Adds to_json() to any class that has attributes."""

    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)


class ReprMixin:
    """Adds a readable __repr__ built from the attributes."""

    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({fields})"


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class SmartProduct(JsonMixin, ReprMixin, Product):
    """Gets to_json() and a nice repr without copying any code."""


# Composition alternative (what the course prefers): HAS-A instead of IS-A
class JsonExporter:
    def export(self, obj) -> str:
        return json.dumps(obj.__dict__, sort_keys=True)


class Catalog:
    def __init__(self, exporter: JsonExporter):
        self.exporter = exporter          # composition: the catalog HAS an exporter
        self.products = []

    def add(self, product):
        self.products.append(product)

    def export_all(self):
        return [self.exporter.export(p) for p in self.products]


if __name__ == "__main__":
    p = SmartProduct("Mug", 12.0)
    print(p)
    print(p.to_json())
    print([c.__name__ for c in SmartProduct.__mro__])
    catalog = Catalog(JsonExporter())
    catalog.add(Product("Cap", 18.0))
    print(catalog.export_all())
