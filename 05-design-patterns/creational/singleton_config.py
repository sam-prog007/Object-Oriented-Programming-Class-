"""Singleton: refactor the configuration manager.

Before: every module calls load_config(), so config.json is read 4 times per request
and each module has its own copy.
After: one ConfigManager instance, loaded once, shared by everyone.
"""

import json
from pathlib import Path

DEFAULT_PATH = Path(__file__).with_name("config.json")


class ConfigManager:
    _instance = None

    def __init__(self, path=DEFAULT_PATH):
        # Guard: the constructor must not be called directly twice.
        if ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.get_instance()")
        self.path = Path(path)
        self.load_count = 0
        self._data = {}
        self._load()

    @classmethod
    def get_instance(cls, path=DEFAULT_PATH) -> "ConfigManager":
        """Create the instance on first call, then always return the same one."""
        if cls._instance is None:
            cls._instance = cls(path)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Forget the instance (used by tests to start fresh)."""
        cls._instance = None

    def _load(self) -> None:
        with open(self.path, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        self.load_count += 1

    def get(self, key: str, default=None):
        """Read a nested value with a dotted key: get("database.host")."""
        value = self._data
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, value) -> None:
        """Change a value; every module sees it, because they share this instance."""
        *parents, last = key.split(".")
        node = self._data
        for part in parents:
            node = node.setdefault(part, {})
        node[last] = value


# The four "modules" from the exercise, now using the shared instance.
def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    print(f"Sending email from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount: float):
    config = ConfigManager.get_instance()
    print(f"Processing {amount}€ in {config.get('payment.environment')} mode")


if __name__ == "__main__":
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)
    config = ConfigManager.get_instance()
    print(f"config.json read {config.load_count} time(s)")   # 1
