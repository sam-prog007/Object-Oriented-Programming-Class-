"""Strategy: refactor the report generator.

Before: generate_report() and save_report() each have an if/elif per format.
After: one strategy class per format, and a ReportGenerator (the context) that
holds a strategy and can switch it at runtime. HTML is added at the end without
touching any existing class.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path


class ReportFormatStrategy(ABC):
    """Contract for every report format."""

    extension = ""

    @abstractmethod
    def format(self, data: list) -> str:
        ...


class PDFFormatStrategy(ReportFormatStrategy):
    extension = ".pdf"

    def format(self, data: list) -> str:
        lines = ["PDF REPORT", "=" * 50]
        lines += [f"| {item['name']:20} | {item['value']:10} |" for item in data]
        lines += ["=" * 50, "End of PDF Report"]
        return "\n".join(lines)


class ExcelFormatStrategy(ReportFormatStrategy):
    extension = ".xlsx"

    def format(self, data: list) -> str:
        lines = ["EXCEL REPORT", "-" * 50, "Name\tValue"]
        lines += [f"{item['name']}\t{item['value']}" for item in data]
        lines.append("-" * 50)
        return "\n".join(lines) + "\n"


class CSVFormatStrategy(ReportFormatStrategy):
    extension = ".csv"

    def format(self, data: list) -> str:
        return "name,value\n" + "".join(f"{item['name']},{item['value']}\n" for item in data)


class JSONFormatStrategy(ReportFormatStrategy):
    extension = ".json"

    def format(self, data: list) -> str:
        return json.dumps(data, indent=2)


class ReportGenerator:
    """The context: knows the data, delegates the formatting to its current strategy."""

    def __init__(self, data: list, strategy: ReportFormatStrategy = None):
        self.data = data
        self._strategy = strategy

    def set_strategy(self, strategy: ReportFormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise ValueError("No format strategy set")
        return self._strategy.format(self.data)

    def save_report(self, filename: str) -> Path:
        path = Path(filename + self._strategy.extension)
        path.write_text(self.generate_report(), encoding="utf-8")
        return path


# --- Final test from the exercise: a new format WITHOUT modifying existing classes ---
class HTMLFormatStrategy(ReportFormatStrategy):
    extension = ".html"

    def format(self, data: list) -> str:
        rows = "".join(f"<tr><td>{item['name']}</td><td>{item['value']}</td></tr>" for item in data)
        return f"<table><tr><th>Name</th><th>Value</th></tr>{rows}</table>"


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]
    generator = ReportGenerator(data)
    for strategy in [PDFFormatStrategy(), CSVFormatStrategy(), JSONFormatStrategy(), HTMLFormatStrategy()]:
        generator.set_strategy(strategy)          # switch format at runtime
        print(f"=== {type(strategy).__name__} ===")
        print(generator.generate_report())
        print()
