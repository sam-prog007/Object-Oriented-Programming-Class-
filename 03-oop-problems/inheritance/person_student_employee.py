"""Inheritance problem 2: Student and Employee extend Person."""


class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, from {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)   # reuse the parent's constructor
        self.field_of_study = field_of_study

    def introduce(self):
        return super().introduce() + f" I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return super().introduce() + f" I work at {self.company}."


if __name__ == "__main__":
    people = [
        Person("Alex", 40, "Lyon"),
        Student("Sam", 20, "Paris", "AI & Data"),
        Employee("Léa", 28, "Paris", "Orange"),
    ]
    for p in people:
        print(p.introduce())
