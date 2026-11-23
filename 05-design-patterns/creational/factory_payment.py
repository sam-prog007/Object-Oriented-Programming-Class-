"""Factory Method: refactor the payment system.

Before: one process_payment() with an if/elif per payment type.
After: one class per payment type behind an abstract interface, and a factory
that maps a name to a class with a dictionary (no if chain).
"""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """The interface every payment processor must follow."""

    name = "abstract"

    @abstractmethod
    def validation_error(self, details: dict):
        """Return an error message if the details are invalid, None if they are fine."""

    @abstractmethod
    def calculate_fee(self, amount: float) -> float:
        """Return the fee for this payment method."""

    def validate(self, details: dict) -> bool:
        return self.validation_error(details) is None

    def process(self, amount: float, details: dict) -> dict:
        # Same workflow for every processor: validate, compute fee, return the result.
        error = self.validation_error(details)
        if error:
            return {"success": False, "error": error}
        fee = round(self.calculate_fee(amount), 2)
        return {"success": True, "method": self.name, "amount": round(amount + fee, 2), "fee": fee}


class CreditCardProcessor(PaymentProcessor):
    name = "credit_card"

    def validation_error(self, details: dict):
        if len(details.get("card_number") or "") != 16:
            return "Invalid card number"
        if len(details.get("cvv") or "") != 3:
            return "Invalid CVV"
        return None

    def calculate_fee(self, amount: float) -> float:
        return amount * 0.029                     # 2.9 %


class BankTransferProcessor(PaymentProcessor):
    name = "bank_transfer"

    def validation_error(self, details: dict):
        return None if len(details.get("iban") or "") >= 15 else "Invalid IBAN"

    def calculate_fee(self, amount: float) -> float:
        return 1.50                               # flat fee


class PayPalProcessor(PaymentProcessor):
    name = "paypal"

    def validation_error(self, details: dict):
        return None if "@" in (details.get("email") or "") else "Invalid PayPal email"

    def calculate_fee(self, amount: float) -> float:
        return amount * 0.034 + 0.30              # 3.4 % + 0.30 €


class PaymentFactory:
    """Turns a string into the right processor. New methods are registered, not coded in."""

    def __init__(self):
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor,
        }

    def register(self, name: str, processor_class: type) -> None:
        """Add a new payment method without modifying any existing class (Open/Closed)."""
        self._processors[name] = processor_class

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        try:
            return self._processors[payment_type]()
        except KeyError:
            raise ValueError(f"Unknown payment type: {payment_type}") from None


if __name__ == "__main__":
    factory = PaymentFactory()

    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    processor = factory.get_processor("bank_transfer")
    print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))

    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "sam@example.com"}))

    # Adding Apple Pay = one new class + one register() call, nothing else changes
    class ApplePayProcessor(PaymentProcessor):
        name = "apple_pay"

        def validation_error(self, details):
            return None if details.get("token") else "Missing Apple Pay token"

        def calculate_fee(self, amount):
            return amount * 0.015

    factory.register("apple_pay", ApplePayProcessor)
    print(factory.get_processor("apple_pay").process(100.0, {"token": "abc"}))
