from pathlib import Path
import yaml


class TestDataLoader:

    def import_report_registration_test_data():
        # 1. Define the path to your file
        yaml_path = Path("testdata/report_registration.yaml")

        # 2. Open and read the file
        with open(yaml_path, "r") as file:
            data = yaml.safe_load(file)

        return data