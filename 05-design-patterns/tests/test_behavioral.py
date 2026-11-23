import json

import pytest

from strategy_report import (
    CSVFormatStrategy,
    ExcelFormatStrategy,
    HTMLFormatStrategy,
    JSONFormatStrategy,
    PDFFormatStrategy,
    ReportFormatStrategy,
    ReportGenerator,
)
from template_etl import APIPipeline, CSVPipeline, DatabasePipeline, DataPipeline, XMLPipeline

DATA = [{"name": "Sales Q1", "value": 15000}, {"name": "Sales Q2", "value": 18000}]


# ----------------------------------------------------------------- Strategy ---
class TestStrategy:
    def test_csv(self):
        assert CSVFormatStrategy().format(DATA) == "name,value\nSales Q1,15000\nSales Q2,18000\n"

    def test_json(self):
        assert json.loads(JSONFormatStrategy().format(DATA)) == DATA

    def test_pdf_and_excel_headers(self):
        assert PDFFormatStrategy().format(DATA).startswith("PDF REPORT")
        assert "Name\tValue" in ExcelFormatStrategy().format(DATA)

    def test_switch_strategy_at_runtime(self):
        gen = ReportGenerator(DATA, CSVFormatStrategy())
        csv = gen.generate_report()
        gen.set_strategy(JSONFormatStrategy())
        assert gen.generate_report() != csv

    def test_html_added_without_changing_other_classes(self):
        gen = ReportGenerator(DATA, HTMLFormatStrategy())
        assert "<td>Sales Q1</td>" in gen.generate_report()

    def test_no_strategy_raises(self):
        with pytest.raises(ValueError):
            ReportGenerator(DATA).generate_report()

    def test_save_uses_strategy_extension(self, tmp_path):
        gen = ReportGenerator(DATA, CSVFormatStrategy())
        path = gen.save_report(str(tmp_path / "sales"))
        assert path.suffix == ".csv" and path.read_text().startswith("name,value")

    def test_strategy_interface_is_abstract(self):
        with pytest.raises(TypeError):
            ReportFormatStrategy()


# ---------------------------------------------------------- Template Method ---
ALL_PIPELINES = [
    (CSVPipeline, "data/users.csv"),
    (APIPipeline, "https://api.example.com/users"),
    (DatabasePipeline, "postgresql://localhost/mydb"),
    (XMLPipeline, "data/orders.xml"),
]


class TestTemplateMethod:
    @pytest.mark.parametrize("cls, source", ALL_PIPELINES)
    def test_steps_run_in_fixed_order(self, cls, source):
        pipeline = cls(source, delay=0)
        pipeline.run()
        assert pipeline.steps == ["connect", "extract", "transform", "validate", "load", "cleanup"]

    @pytest.mark.parametrize("cls, source", ALL_PIPELINES)
    def test_result_message_and_cleanup(self, cls, source):
        pipeline = cls(source, delay=0)
        assert pipeline.run() == f"{cls.source_type} Pipeline finished"
        assert pipeline.data is None

    def test_csv_transform(self):
        data = CSVPipeline("x", delay=0).transform([{"id": 1, "name": "bob", "age": "25"}])
        assert data == [{"id": 1, "name": "BOB", "age": 25}]

    def test_api_grade(self):
        data = APIPipeline("x", delay=0).transform([{"user_id": 1, "username": "X", "score": "95"}])
        assert data[0]["grade"] == "A" and data[0]["username"] == "x"

    def test_database_tax(self):
        data = DatabasePipeline("x", delay=0).transform([{"product_id": 1, "product_name": "a", "price": 100}])
        assert data[0]["tax"] == 20.0

    def test_validation_rejects_bad_records(self):
        with pytest.raises(ValueError, match="Invalid record structure"):
            CSVPipeline("x", delay=0).validate([{"name": "no id"}])

    def test_hook_runs_before_workflow(self, mocker):
        pipeline = APIPipeline("x", delay=0)
        hook = mocker.spy(pipeline, "before_run")
        pipeline.run()
        hook.assert_called_once()

    def test_base_class_is_abstract(self):
        with pytest.raises(TypeError):
            DataPipeline("x")
