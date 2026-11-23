"""Inheritance problem 3: BankAccount and SavingsAccount."""


class BankAccount:
    def __init__(self, account_number, balance=0.0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount

    def transfer(self, destination, amount):
        """Move money to another account. False if the balance is too low."""
        if amount <= 0 or amount > self.balance:
            return False
        self.withdraw(amount)          # reuse existing methods
        destination.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0.0, interest_rate=0.03):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self):
        return self.balance


if __name__ == "__main__":
    current = BankAccount("FR-001", 500)
    savings = SavingsAccount("FR-002", 1000, interest_rate=0.05)

    print(current.transfer(savings, 200))   # True
    print(current.transfer(savings, 9999))  # False, not enough money
    savings.add_interest()                  # +5% of 1200 = 60
    print(savings.check_balance())          # 1260.0
    print(current.balance)                  # 300
