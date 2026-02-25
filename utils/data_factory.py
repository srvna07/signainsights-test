import random
import string
import yaml
import random
from datetime import datetime
from pathlib import Path

class DataFactory:

    @staticmethod
    def random_string(length=6):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def random_username(prefix="user_"):
        return prefix + DataFactory.random_string()

    @staticmethod
    def random_email(prefix="user_", domain="@gmail.com"):
        return prefix + DataFactory.random_string() + domain

    @staticmethod
    def random_org_name(prefix="Test_Org_Name"):
        return prefix + DataFactory.random_string()
    
    @staticmethod
    def random_string(length=4):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_report_name(prefix="Test_Report"):
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def generate_menu_name(prefix="Test_Menu"):
        return f"{prefix}_{DataFactory.random_string()}"

    @staticmethod
    def generate_organization_name(prefix="Test_Organization"):
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{prefix}_{suffix}"

    
