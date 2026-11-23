"""super() follows the MRO, not "my parent".

Every class calls super().greet(), so each class in the MRO runs exactly ONCE,
in MRO order, and the shared base (Base) runs last, only once.
"""


class Base:
    def greet(self, log):
        log.append("Base")


class Left(Base):
    def greet(self, log):
        log.append("Left")
        super().greet(log)       # inside Left, for a Child object, this goes to Right!


class Right(Base):
    def greet(self, log):
        log.append("Right")
        super().greet(log)


class Child(Left, Right):
    def greet(self, log):
        log.append("Child")
        super().greet(log)


if __name__ == "__main__":
    log = []
    Child().greet(log)
    print(" -> ".join(log))      # Child -> Left -> Right -> Base
    print([c.__name__ for c in Child.__mro__])
