import pytest

from circle import Circle
from complex_number import Complex
from matrix import Matrix
from person import Person
from point import Point
from vector import Vector


class TestComplex:
    def test_addition(self):
        assert Complex(3, 2) + Complex(1, 4) == Complex(4, 6)

    def test_subtraction(self):
        assert Complex(3, 2) - Complex(1, 4) == Complex(2, -2)

    def test_str_positive_and_negative(self):
        assert str(Complex(4, 6)) == "4 + 6i"
        assert str(Complex(2, -2)) == "2 - 2i"

    def test_returns_new_object(self):
        a, b = Complex(1, 1), Complex(2, 2)
        c = a + b
        assert c is not a and a == Complex(1, 1)


class TestPerson:
    def test_older_is_greater(self):
        assert Person("Alice", 30, "F") > Person("Bob", 25, "M")

    def test_younger_is_not_greater(self):
        assert not Person("Bob", 25, "M") > Person("Alice", 30, "F")

    def test_same_age_is_not_greater(self):
        assert not Person("A", 20, "F") > Person("B", 20, "M")


class TestVector:
    def test_dot_product(self):
        assert Vector(1, 2, 3) * Vector(4, 5, 6) == 32

    def test_orthogonal_vectors(self):
        assert Vector(1, 0, 0) * Vector(0, 1, 0) == 0


class TestCircle:
    def test_all_six_operators(self):
        small, big = Circle(2), Circle(5)
        assert small < big and small <= big
        assert big > small and big >= small
        assert small != big and not small == big
        assert Circle(3) == Circle(3)

    def test_sorting_uses_lt(self):
        radii = [c.radius for c in sorted([Circle(3), Circle(1), Circle(2)])]
        assert radii == [1, 2, 3]

    def test_negative_radius_rejected(self):
        with pytest.raises(ValueError):
            Circle(-1)


class TestPoint:
    def test_distance(self):
        assert Point(3, 4).distance() == 5.0

    def test_comparisons(self):
        near, far = Point(1, 1), Point(3, 4)
        assert near < far and near <= far
        assert far > near and far >= near
        assert near != far

    def test_different_points_same_distance_are_equal(self):
        assert Point(3, 4) == Point(0, 5)


class TestMatrix:
    def test_square_product(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        assert a * b == Matrix([[19, 22], [43, 50]])

    def test_rectangular_product(self):
        a = Matrix([[1, 2, 3]])          # 1x3
        b = Matrix([[1], [2], [3]])      # 3x1
        assert a * b == Matrix([[14]])   # 1x1

    def test_incompatible_sizes(self):
        with pytest.raises(ValueError):
            Matrix([[1, 2]]) * Matrix([[1, 2]])
