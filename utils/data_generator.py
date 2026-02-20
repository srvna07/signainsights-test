import yaml
import random
import string
from datetime import datetime
from pathlib import Path


class DataGenerator:

    # Adjust this path if needed
    DATA_FILE = Path("testdata/report_registration.yaml")

    @staticmethod
    def random_string(length=4):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_report_name(prefix="Test_Report"):
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def generate_menu_name(prefix="Test_Menu"):
        return f"{prefix}_{DataGenerator.random_string()}"

    @classmethod
    def update_report_fields(cls):
        if not cls.DATA_FILE.exists():
            raise FileNotFoundError(f"{cls.DATA_FILE} not found")

        with open(cls.DATA_FILE, "r") as file:
            data = yaml.safe_load(file)

        data["new_report"]["report_name"] = cls.generate_report_name()
        data["new_report"]["menu_name"] = cls.generate_menu_name()
        data["edit_report"]["report_name"] = cls.generate_report_name("Edited_Report")

        with open(cls.DATA_FILE, "w") as file:
            yaml_string = yaml.dump(data, sort_keys=False)
            yaml_string = yaml_string.replace("\nedit_report:", "\n\nedit_report:")
            file.write(yaml_string)

        print("YAML updated successfully.")
        return data


# Allow standalone execution
if __name__ == "__main__":
    DataGenerator.update_report_fields()