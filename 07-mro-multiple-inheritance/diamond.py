r"""Slide 37: the diamond problem. Which who_am_i() does D call?

        A
       / \
      B   C
       \ /
        D
"""


class A:
    def who_am_i(self):
        return "Class A"


class B(A):
    def who_am_i(self):
        return "Class B"


class C(A):
    def who_am_i(self):
        return "Class C"


class D(B, C):          # parents read LEFT to RIGHT: B first
    pass


class E(C, B):          # same parents, other order: C first
    pass


class BNoMethod(A):     # a B that does NOT define who_am_i
    pass


class G(BNoMethod, C):  # trap: the answer is C, not A
    pass


def mro_names(cls):
    """Readable MRO: ['D', 'B', 'C', 'A', 'object']."""
    return [k.__name__ for k in cls.__mro__]


if __name__ == "__main__":
    for cls in (D, E, G):
        print(f"{cls.__name__}().who_am_i() -> {cls().who_am_i():8}  MRO: {mro_names(cls)}")
    print(type(D.__mro__).__name__, type(D.mro()).__name__)   # tuple list
