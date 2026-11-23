"""Inheritance problem 1: Car and Bicycle override Vehicle.drive()."""


class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):          # overriding: same name, new behaviour
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


if __name__ == "__main__":
    # polymorphism: the same call gives a different result depending on the real class
    for v in [Vehicle(), Car(), Bicycle()]:
        print(v.drive())
