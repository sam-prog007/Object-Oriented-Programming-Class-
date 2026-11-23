"""Problem 1: complex numbers with + and -."""


class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        # (a + bi) + (c + di) = (a + c) + (b + d)i
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        # (a + bi) - (c + di) = (a - c) + (b - d)i
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __str__(self):
        sign = "-" if self.imag < 0 else "+"
        return f"{self.real} {sign} {abs(self.imag)}i"

    def __repr__(self):
        return f"Complex({self.real}, {self.imag})"


if __name__ == "__main__":
    a = Complex(3, 2)
    b = Complex(1, 4)
    print(a + b)   # 4 + 6i
    print(a - b)   # 2 - 2i
