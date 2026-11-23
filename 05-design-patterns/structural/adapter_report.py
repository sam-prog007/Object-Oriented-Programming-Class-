"""Adapter: plug the legacy XML report generator into the JSON dashboard.

Before: every function converts the format by hand (and cheats by re-using the
original dict instead of the XML).
After: one adapter wraps the legacy class and really converts its XML into JSON.
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


# --- Legacy system: an external library we are NOT allowed to modify ---------------
class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system"""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


# --- New system ------------------------------------------------------------------------
class AnalyticsDashboard:
    def display(self, json_data: str) -> None:
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


class ReportGeneratorInterface(ABC):
    """What the dashboard side expects: generate(data) returns a JSON string."""

    @abstractmethod
    def generate(self, data: dict) -> str:
        ...


# --- The adapter -------------------------------------------------------------------------
class LegacyReportAdapter(ReportGeneratorInterface):
    """Wraps LegacyReportGenerator and translates its XML output into JSON."""

    def __init__(self, legacy: LegacyReportGenerator):
        self._legacy = legacy

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)
        root = ET.fromstring(xml_report)
        converted = {child.tag: self._parse_value(child.text) for child in root}
        return json.dumps(converted)

    @staticmethod
    def _parse_value(text):
        """XML only stores text: turn '1234' back into 1234 and '121.55' into 121.55."""
        text = (text or "").strip()
        for cast in (int, float):
            try:
                return cast(text)
            except ValueError:
                pass
        return text


# --- Business code: no format conversion anywhere ----------------------------------------
def show_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard, data: dict):
    dashboard.display(generator.generate(data))


if __name__ == "__main__":
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    show_report(report_generator, dashboard, {"total_sales": 150000, "orders": 1234, "avg_order": 121.55})
    show_report(report_generator, dashboard, {"total_items": 5000, "low_stock": 45, "out_of_stock": 12})
