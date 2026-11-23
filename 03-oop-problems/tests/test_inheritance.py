import pytest

from bank_account import BankAccount, SavingsAccount
from person_student_employee import Employee, Person, Student
from vehicle import Bicycle, Car, Vehicle


class TestVehicle:
    def test_each_class_overrides_drive(self):
        assert Vehicle().drive() == "Driving a vehicle"
        assert Car().drive() == "Driving a car"
        assert Bicycle().drive() == "Riding a bicycle"

    def test_subclasses_are_vehicles(self):
        assert isinstance(Car(), Vehicle) and isinstance(Bicycle(), Vehicle)


class TestPersonHierarchy:
    def test_student_keeps_parent_attributes(self):
        s = Student("Sam", 20, "Paris", "AI")
        assert (s.name, s.age, s.address, s.field_of_study) == ("Sam", 20, "Paris", "AI")

    def test_introductions_are_personalised(self):
        assert "study AI" in Student("Sam", 20, "Paris", "AI").introduce()
        assert "work at Orange" in Employee("Léa", 28, "Paris", "Orange").introduce()
        assert "study" not in Person("Alex", 40, "Lyon").introduce()


class TestBankAccount:
    def test_deposit_and_withdraw(self):
        acc = BankAccount("A", 100)
        acc.deposit(50)
        acc.withdraw(30)
        assert acc.balance == 120

    def test_withdraw_too_much_raises(self):
        with pytest.raises(ValueError):
            BankAccount("A", 10).withdraw(100)

    def test_transfer_success(self):
        a, b = BankAccount("A", 100), BankAccount("B", 0)
        assert a.transfer(b, 40) is True
        assert (a.balance, b.balance) == (60, 40)

    def test_transfer_insufficient_balance(self):
        a, b = BankAccount("A", 10), BankAccount("B", 0)
        assert a.transfer(b, 40) is False
        assert (a.balance, b.balance) == (10, 0)


class TestSavingsAccount:
    def test_interest(self):
        s = SavingsAccount("S", 1000, interest_rate=0.05)
        assert s.add_interest() == 50
        assert s.check_balance() == 1050

    def test_inherits_transfer(self):
        s, a = SavingsAccount("S", 100), BankAccount("A", 0)
        assert s.transfer(a, 100) is True
        assert s.check_balance() == 0
