import math

import pytest

from shapes_abc import Arrow, BrokenSquare, Circle, Drawable, Rectangle, Shape, Smiley, render


class TestABC:
    def test_abc_cannot_be_instantiated(self):
        with pytest.raises(TypeError, match="abstract"):
            Shape()

    def test_incomplete_subclass_fails_at_creation(self):
        with pytest.raises(TypeError, match="perimeter"):
            BrokenSquare(2)

    def test_concrete_subclasses(self):
        assert Rectangle(2, 3).area() == 6
        assert Circle(1).perimeter() == pytest.approx(2 * math.pi)

    def test_concrete_method_is_inherited(self):
        assert Rectangle(2, 3).describe() == "Rectangle: area=6.00, perimeter=10.00"

    def test_polymorphism(self):
        total = sum(s.area() for s in [Rectangle(1, 1), Rectangle(2, 2)])
        assert total == 5


class TestProtocol:
    def test_no_inheritance_needed(self):
        assert Drawable not in Smiley.__mro__
        assert isinstance(Smiley(), Drawable)

    def test_object_without_draw_is_not_drawable(self):
        assert not isinstance(Circle(1), Drawable)

    def test_render_works_with_any_drawable(self):
        assert render([Smiley(), Arrow()]) == ":-) --->"
