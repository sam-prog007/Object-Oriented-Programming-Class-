"""Template Method: refactor the ETL pipelines.

Before: CSVPipeline, APIPipeline and DatabasePipeline each copy the whole
connect / extract / transform / validate / load / cleanup workflow.
After: the workflow is written once in DataPipeline.run(); subclasses only
fill in what is specific to them. XMLPipeline proves it is easy to extend.
"""

import time
from abc import ABC, abstractmethod


class DataPipeline(ABC):
    """Abstract base class holding the template method run()."""

    source_type = "source"
    required_fields: tuple = ()

    def __init__(self, source: str, delay: float = 0.5):
        self.source = source
        self.delay = delay            # simulated network / disk time (0 in tests)
        self.data = None
        self.steps = []               # records the order of steps (useful in tests)

    # ---- the TEMPLATE METHOD: the workflow is fixed here and cannot be skipped ----
    def run(self) -> str:
        self.before_run()             # hook
        self.connect()
        self.data = self.extract()
        print(f"Extracted {len(self.data)} records")
        self.data = self.transform(self.data)
        self.validate(self.data)
        self.load(self.data)
        self.cleanup()
        self.after_run()              # hook
        return f"{self.source_type} Pipeline finished"

    # ---- steps every subclass MUST implement ----
    @abstractmethod
    def extract(self) -> list:
        ...

    @abstractmethod
    def transform(self, data: list) -> list:
        ...

    # ---- common steps, written once ----
    def connect(self) -> None:
        self.steps.append("connect")
        print(f"Connecting to {self.source_type}: {self.source}")
        time.sleep(self.delay)
        print(f"{self.source_type} connection established")

    def validate(self, data: list) -> None:
        self.steps.append("validate")
        print("Validating data...")
        for record in data:
            if any(field not in record for field in self.required_fields):
                raise ValueError("Invalid record structure")
        print("Validation passed")

    def load(self, data: list) -> None:
        self.steps.append("load")
        print("Loading data to destination...")
        time.sleep(self.delay)
        print(f"Loaded {len(data)} records successfully")

    def cleanup(self) -> None:
        self.steps.append("cleanup")
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")

    # ---- hooks: optional, empty by default, subclasses MAY override ----
    def before_run(self) -> None:
        pass

    def after_run(self) -> None:
        pass


class CSVPipeline(DataPipeline):
    source_type = "CSV"
    required_fields = ("id", "name")

    def extract(self) -> list:
        self.steps.append("extract")
        return [{"id": 1, "name": "Alice", "age": "30"}, {"id": 2, "name": "Bob", "age": "25"}]

    def transform(self, data: list) -> list:
        self.steps.append("transform")
        for record in data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()
        return data


class APIPipeline(DataPipeline):
    source_type = "API"
    required_fields = ("user_id", "username")

    def extract(self) -> list:
        self.steps.append("extract")
        return [{"user_id": 101, "username": "Charlie", "score": "85"},
                {"user_id": 102, "username": "Diana", "score": "92"}]

    def transform(self, data: list) -> list:
        self.steps.append("transform")
        for record in data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"
        return data

    def before_run(self) -> None:          # hook used only here
        print("Checking API rate limit...")


class DatabasePipeline(DataPipeline):
    source_type = "Database"
    required_fields = ("product_id", "price")

    def extract(self) -> list:
        self.steps.append("extract")
        return [{"product_id": 501, "product_name": "laptop", "price": 1200},
                {"product_id": 502, "product_name": "mouse", "price": 25}]

    def transform(self, data: list) -> list:
        self.steps.append("transform")
        for record in data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2
        return data


class XMLPipeline(DataPipeline):
    """The new pipeline from the exercise: only the XML-specific parts are written."""

    source_type = "XML"
    required_fields = ("order_id", "amount")

    def extract(self) -> list:
        import xml.etree.ElementTree as ET
        self.steps.append("extract")
        xml = ("<orders><order><order_id>9001</order_id><amount>49.90</amount></order>"
               "<order><order_id>9002</order_id><amount>15</amount></order></orders>")
        return [{child.tag: child.text for child in order} for order in ET.fromstring(xml)]

    def transform(self, data: list) -> list:
        self.steps.append("transform")
        for record in data:
            record["order_id"] = int(record["order_id"])
            record["amount"] = float(record["amount"])
        return data


if __name__ == "__main__":
    pipelines = [
        CSVPipeline("data/users.csv"),
        APIPipeline("https://api.example.com/users"),
        DatabasePipeline("postgresql://localhost/mydb"),
        XMLPipeline("data/orders.xml"),
    ]
    for pipeline in pipelines:
        print(f"RUNNING {pipeline.source_type.upper()} PIPELINE")
        print("=" * 70)
        print(f"\n{pipeline.run()}\n")
