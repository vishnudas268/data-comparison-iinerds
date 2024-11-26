import pandas as ps


class CSVReport:
    def __init__(self, source_csv_data, output_csv_data, report_csv_data):
        self.source_csv = source_csv_data
        self.output_csv = output_csv_data
        self.report_csv = report_csv_data

    def generate_report(self):
        source_data = ps.read_csv(self.source_csv)
        output_data = ps.read_csv(self.output_csv)

        compare_csv = source_data.columns.intersection(source_data.columns)

        report_data = []
