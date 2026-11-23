import json

import pytest

from builder_employee import DeveloperBuilder, Employee, EmployeeBuilder, InternBuilder
from factory_payment import (
    BankTransferProcessor,
    CreditCardProcessor,
    PaymentFactory,
    PaymentProcessor,
    PayPalProcessor,
)
from singleton_config import ConfigManager


# ------------------------------------------------------------------ Factory ---
class TestFactory:
    @pytest.fixture
    def factory(self):
        return PaymentFactory()

    @pytest.mark.parametrize("name, cls", [
        ("credit_card", CreditCardProcessor),
        ("bank_transfer", BankTransferProcessor),
        ("paypal", PayPalProcessor),
    ])
    def test_factory_returns_right_class(self, factory, name, cls):
        assert isinstance(factory.get_processor(name), cls)

    def test_unknown_type_raises(self, factory):
        with pytest.raises(ValueError, match="Unknown payment type"):
            factory.get_processor("bitcoin")

    def test_credit_card_fee(self, factory):
        result = factory.get_processor("credit_card").process(
            100.0, {"card_number": "1234567890123456", "cvv": "123"})
        assert result == {"success": True, "method": "credit_card", "amount": 102.9, "fee": 2.9}

    def test_credit_card_invalid_number_and_cvv(self, factory):
        p = factory.get_processor("credit_card")
        assert p.process(100, {"card_number": "123", "cvv": "123"})["error"] == "Invalid card number"
        assert p.process(100, {"card_number": "1234567890123456", "cvv": "1"})["error"] == "Invalid CVV"

    def test_bank_transfer_flat_fee(self, factory):
        result = factory.get_processor("bank_transfer").process(100.0, {"iban": "FR7630006000011234567890189"})
        assert result["fee"] == 1.5 and result["amount"] == 101.5

    def test_paypal_fee_and_validation(self, factory):
        p = factory.get_processor("paypal")
        assert p.process(100.0, {"email": "a@b.com"})["fee"] == 3.7
        assert p.process(100.0, {"email": "nope"})["error"] == "Invalid PayPal email"

    def test_register_new_method_without_editing_code(self, factory):
        class CryptoProcessor(PaymentProcessor):
            name = "crypto"

            def validation_error(self, details):
                return None

            def calculate_fee(self, amount):
                return 0.0

        factory.register("crypto", CryptoProcessor)
        assert factory.get_processor("crypto").process(10, {})["success"] is True

    def test_interface_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            PaymentProcessor()


# ------------------------------------------------------------------ Builder ---
class TestBuilder:
    def test_fluent_build(self):
        e = (EmployeeBuilder().with_name("John", "Doe").with_email("john@co.com")
             .with_job("Engineering", "Dev", 50000).with_equipment(laptop=True)
             .with_access(vpn=True).build())
        assert isinstance(e, Employee)
        assert e.has_laptop and e.has_vpn_access and not e.has_admin_rights

    def test_chainable_methods_return_builder(self):
        b = EmployeeBuilder()
        assert b.with_name("A", "B") is b

    def test_missing_name_rejected(self):
        with pytest.raises(ValueError, match="Name is required"):
            EmployeeBuilder().with_email("a@b.com").with_job("X", "Y", 1).build()

    def test_invalid_email_rejected(self):
        with pytest.raises(ValueError, match="email"):
            EmployeeBuilder().with_name("A", "B").with_email("nope").with_job("X", "Y", 1).build()

    def test_negative_salary_rejected(self):
        with pytest.raises(ValueError, match="negative"):
            EmployeeBuilder().with_name("A", "B").with_email("a@b.com").with_job("X", "Y", -5).build()

    def test_developer_preset_always_has_admin_rights(self):
        dev = DeveloperBuilder("John", "Doe", "john@co.com").build()
        assert dev.has_admin_rights and dev.has_laptop and dev.department == "Engineering"

    def test_intern_preset(self):
        intern = InternBuilder("Jane", "Smith", "jane@co.com", "Marketing", 42).build()
        assert intern.contract_type == "internship" and intern.manager_id == 42
        assert not intern.has_admin_rights


# ---------------------------------------------------------------- Singleton ---
class TestSingleton:
    @pytest.fixture(autouse=True)
    def fresh_singleton(self):
        ConfigManager.reset()
        yield
        ConfigManager.reset()

    def test_same_instance(self):
        assert ConfigManager.get_instance() is ConfigManager.get_instance()

    def test_file_read_only_once(self):
        for _ in range(5):
            ConfigManager.get_instance()
        assert ConfigManager.get_instance().load_count == 1

    def test_dotted_get(self):
        config = ConfigManager.get_instance()
        assert config.get("database.host") == "localhost"
        assert config.get("database.port") == 5432
        assert config.get("app.debug") is True
        assert config.get("does.not.exist", "default") == "default"

    def test_change_is_seen_everywhere(self):
        ConfigManager.get_instance().set("app.debug", False)
        assert ConfigManager.get_instance().get("app.debug") is False

    def test_direct_constructor_blocked(self):
        ConfigManager.get_instance()
        with pytest.raises(RuntimeError):
            ConfigManager()

    def test_custom_file(self, tmp_path):
        path = tmp_path / "config.json"
        path.write_text(json.dumps({"app": {"name": "Test"}}))
        assert ConfigManager.get_instance(path).get("app.name") == "Test"
