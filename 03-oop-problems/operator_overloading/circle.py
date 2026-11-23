"""Problem 5: all six comparison operators for Circle, based on the radius."""


class Circle:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius

    def __lt__(self, other):   # <
        return self.radius < other.radius

    def __le__(self, other):   # <=
        return self.radius <= other.radius

    def __gt__(self, other):   # >
        return self.radius > other.radius

    def __ge__(self, other):   # >=
        return self.radius >= other.radius

    def __eq__(self, other):   # ==
        return self.radius == other.radius

    def __ne__(self, other):   # !=
        return self.radius != other.radius

    def __repr__(self):
        return f"Circle({self.radius})"


if __name__ == "__main__":
    small, big = Circle(2), Circle(5)
    print(small < big, small <= big, small > big)    # True True False
    print(small >= big, small == big, small != big)  # False False True
    print(sorted([Circle(3), Circle(1), Circle(2)]))  # sorted() works thanks to __lt__
