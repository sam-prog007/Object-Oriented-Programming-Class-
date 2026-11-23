"""Slides 61-64: Abstract Base Class vs Protocol, on the same shapes example."""

import math
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------- ABC version ---
class Shape(ABC):
    """Cannot be instantiated. Mixes abstract methods (contract) and concrete ones (shared code)."""

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:            # concrete: inherited by every shape
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class BrokenSquare(Shape):
    """Forgets perimeter(): Python refuses to create it (TypeError at instantiation)."""

    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


# ----------------------------------------------------------- Protocol version ---
@runtime_checkable
class Drawable(Protocol):
    """Structural typing: ANY class with a draw() method fits, no inheritance needed."""

    def draw(self) -> str:
        ...


class Smiley:                       # does NOT inherit from Drawable
    def draw(self) -> str:
        return ":-)"


class Arrow:
    def draw(self) -> str:
        return "--->"


def render(items: list[Drawable]) -> str:
    return " ".join(item.draw() for item in items)


if __name__ == "__main__":
    for shape in (Circle(1), Rectangle(2, 3)):
        print(shape.describe())
    try:
        Shape()
    except TypeError as e:
        print("Shape():", e)
    try:
        BrokenSquare(2)
    except TypeError as e:
        print("BrokenSquare(2):", e)
    print(render([Smiley(), Arrow()]))
    print(isinstance(Smiley(), Drawable))    # True, thanks to @runtime_checkable
