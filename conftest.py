import os
import pytest
import logging
import yaml
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.env_loader import load_env
from utils.logger import get_logger
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.newuser_page import NewUserPage
from pages.organizations_page import NewOrganizationPage
from pages.report_registration_page import ReportRegistrationPageActions
from pages.landing_page import LandingPage


logger = logging.getLogger(__name__)
logger = get_logger(__name__)

# Load Global Config (Project-wide)
ENV = load_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")

# --------------------------------------------------------------------
# 1. Browser & Session Fixtures 
# --------------------------------------------------------------------
@pytest.fixture(scope="session")
def page():
    """Creates browser, context, and a single page for all tests (session-scoped)."""

    with sync_playwright() as p:
        browser = getattr(p, config["browser"]).launch(headless=config["headless"],args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Apply timeouts
        page.set_default_timeout(config["default_timeout"])
        page.set_default_navigation_timeout(config["navigation_timeout"])

        logger.info(f"ENV: {ENV} | Base URL: {config['base_url']}")
        logger.info(f"Browser: {config['browser']} | Headless: {config['headless']}")

        yield page

        context.close()
        browser.close()

@pytest.fixture(scope="session")
def authenticated_page(page):
    """Logs in once and reuses the session for all 50 tests."""
    login = LoginPage(page)
    login.navigate(config["base_url"])
    # Uses Environment Variables for security
    login.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    logger.info("✓ Session authenticated. Reusing for all tests.")
    return page

@pytest.fixture(scope="session")
def config_fixture():
    """Provides the loaded configuration dictionary to any test that needs it."""
    return config

#----------------------------------------------------------------
# 2. Page Object Fixtures
# ---------------------------------------------------------------
@pytest.fixture
def login_page(page): return LoginPage(page)

@pytest.fixture
def landing_page(page): return LandingPage(page)

@pytest.fixture
def new_user_page(page): return NewUserPage(page)

@pytest.fixture
def new_organization_page(page): return NewOrganizationPage(page)

@pytest.fixture
def report_registration_page(page): return ReportRegistrationPageActions(page)


# -------------------------------------------------------------------
# 3. Data Fixtures 
# -------------------------------------------------------------------

# I. Data Loader Fixtures (The Standard Way) ------------------------
@pytest.fixture(scope="session")
def report_registration_data():
    # Load BOTH data files
    report_data = DataReader.load_yaml("testdata/report_registration.yaml")
    org_data = DataReader.load_yaml("testdata/new_organization.yaml")
    
    # Generate names
    report_data["new_report"]["report_name"] = DataFactory.generate_report_name()
    report_data["new_report"]["menu_name"] = DataFactory.generate_menu_name()
    report_data["edit_report"]["report_name"] = DataFactory.generate_report_name("Edited_Report")
    report_data["organization"] = org_data["organization"]

    return report_data

@pytest.fixture(scope="session")
def update_user_data():
    return DataReader.load_yaml("testdata/update_user.yaml")

@pytest.fixture(scope="session")
def update_organization_data():
    return DataReader.load_yaml("testdata/update_organization.yaml")


# II. Dynamic/Shared Data Fixtures -----------------------------------
@pytest.fixture(scope="session")
def new_user_data():
    """Generates unique user data once for the session."""
    data = DataReader.load_yaml("testdata/new_user.yaml")
    prefix = data["user"]["usernamePrefix"]
    data["user"]["username"] = DataFactory.random_username(prefix)
    data["user"]["email"] = DataFactory.random_email(prefix, data["user"]["emailDomain"])
    return data

@pytest.fixture(scope="session")
def new_organization_data():
    """Generates unique Org data once for the session."""
    data = DataReader.load_yaml("testdata/new_organization.yaml")
    data["organization"]["namePrefix"] = DataFactory.random_org_name(data["organization"]["namePrefix"])
    data["organization"]["franchise_id"] = DataFactory.random_string()
    return data

# --------------------------------------------------------------------
# 4. Hooks (Failure Handling) 
# --------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("authenticated_page") or item.funcargs.get("page")
        if page:
            screenshots_dir = Path(__file__).parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{item.name.replace('/', '_')}_{timestamp}.png"
            page.screenshot(path=str(screenshots_dir / filename), full_page=True)
            print(f"\n📸 Screenshot captured: {filename}")


# --------------------------------------------------------------------
# 5. Extras
# --------------------------------------------------------------------

@pytest.fixture
def import_report_test_data():
    from utils.data_generator import DataGenerator
    # This calls your existing logic to update and return the YAML data
    return DataGenerator.update_report_fields()

@pytest.fixture
def report_test_data():
    """Reads report data from the YAML file in root > testdata"""
    # Get the path to the root directory
    base_path = os.path.abspath(os.path.dirname(__file__))
    yaml_path = os.path.join(base_path, "testdata", "report_registration.yaml")
    
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    
    return data




