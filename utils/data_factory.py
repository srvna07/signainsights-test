import random
import string

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
    def random_org_name(prefix="Org_"):
        return prefix + DataFactory.random_string()

    
