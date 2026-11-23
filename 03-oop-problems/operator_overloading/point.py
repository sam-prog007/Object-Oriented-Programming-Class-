"""Problem 6: compare 2D points by their Euclidean distance from the origin."""

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        """Distance from the origin: sqrt(x² + y²)."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __le__(self, other):
        return self.distance() <= other.distance()

    def __gt__(self, other):
        return self.distance() > other.distance()

    def __ge__(self, other):
        return self.distance() >= other.distance()

    def __eq__(self, other):
        # math.isclose avoids float rounding surprises
        return math.isclose(self.distance(), other.distance())

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


if __name__ == "__main__":
    a, b = Point(3, 4), Point(1, 1)
    print(a.distance())        # 5.0
    print(a > b)               # True
    print(Point(3, 4) == Point(0, 5))   # True: different points, same distance
