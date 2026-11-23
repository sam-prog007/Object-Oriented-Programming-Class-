"""Problem 2: compare two persons by age with >."""


class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        # a comparison dunder returns a boolean, not a new object
        return self.age > other.age

    def __repr__(self):
        return f"Person({self.name!r}, {self.age}, {self.gender!r})"


if __name__ == "__main__":
    p1 = Person("Alice", 30, "F")
    p2 = Person("Bob", 25, "M")
    print(p1 > p2)   # True
    print(p2 > p1)   # False
