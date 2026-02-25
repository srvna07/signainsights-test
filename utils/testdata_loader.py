import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class TestDataLoader:
    
    @staticmethod
    def _load_file(filename: str):
        yaml_path = PROJECT_ROOT / "testdata" / filename
        
        with open(yaml_path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def import_report_registration_test_data():
        return TestDataLoader._load_file("report_registration.yaml")
    
    @staticmethod
    def import_new_organization_test_data():
        return TestDataLoader._load_file("new_organization.yaml")