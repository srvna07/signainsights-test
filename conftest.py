import os
import pytest
from playwright.sync_api import sync_playwright
from utils.env_loader import load_env
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.newuser_page import NewUserPage
from pages.organizations_page import NewOrganizationPage
from pages.landing_page import LandingPage
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from pages.organizations_page import NewOrganizationPage
from pathlib import Path
from datetime import datetime
import random
import string
import logging


logger = logging.getLogger(__name__)
logger = get_logger(__name__)

# Load ENV + YAML Config
ENV = load_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")


# ---------------------------
# Browser + Page Fixture
# ---------------------------
@pytest.fixture(scope="session")
def page():
    """Creates browser, context, and a single page for all tests (session-scoped)."""

    with sync_playwright() as p:
        browser = getattr(p, config["browser"]).launch(headless=config["headless"])
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Apply timeouts
        page.set_default_timeout(config["default_timeout"])
        page.set_default_navigation_timeout(config["navigation_timeout"])

        logger.info(f"ENV: {ENV} | Base URL: {config['base_url']}")
        logger.info(f"Browser: {config['browser']} | Headless: {config['headless']}")

        yield page

        context.close()
        browser.close()


# ---------------------------
# Config Fixture
# ---------------------------
@pytest.fixture(scope="session")
def config_fixture():
    """Returns loaded YAML config."""
    return config


# ---------------------------
# Page Object Fixtures
# ---------------------------
@pytest.fixture
def login_page(page):
    """Provides LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def forgot_password_page(page):
    """Provides ForgotPasswordPage instance."""
    return ForgotPasswordPage(page)


@pytest.fixture
def landing_page(page):
    """Provides LandingPage instance."""
    return LandingPage(page)


@pytest.fixture
def new_user_page(page):
    return NewUserPage(page)

@pytest.fixture
def update_user_data():
    """Load update user test data."""
    return DataReader.load_yaml("testdata/update_user.yaml")
    
# ---------------------------
# Authenticated Session Fixture
# ---------------------------
@pytest.fixture(scope="session")
def authenticated_page(page):
    """
    Uses the SAME Playwright session from the `page` fixture.
    No new sync_playwright() call → no asyncio conflict.
    """
    # Login once on the shared session page
    login = LoginPage(page)
    login.navigate(config["base_url"])
    login.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))

    logger.info("✓ Logged in (session-based authentication). Reusing page…")

    return page

@pytest.fixture(scope="session")
def new_user_data():
    """Loads new user test data + injects random username & email."""
    data = DataReader.load_yaml("testdata/new_user.yaml")

    prefix = data["user"]["usernamePrefix"]
    domain = data["user"]["emailDomain"]

    data["user"]["username"] = DataFactory.random_username(prefix)
    data["user"]["email"] = DataFactory.random_email(prefix, domain)

    return data

@pytest.fixture
def import_report_test_data():
    from utils.data_generator import DataGenerator
    # This calls your existing logic to update and return the YAML data
    return DataGenerator.update_report_fields()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture screenshots on test failure.
    """
    # execute all other hooks to get the report object
    outcome = yield
    rep = outcome.get_result()

    # only act after the test body has run and if it failed
    if rep.when == "call" and rep.failed:
        # Try to get the Playwright page from fixture names
        page = item.funcargs.get("authenticated_page") or item.funcargs.get("page")
        if page:
            # Create screenshots directory if it doesn't exist
            # screenshots_dir = Path("screenshots")
            screenshots_dir = Path(__file__).parent / "screenshots"

            screenshots_dir.mkdir(exist_ok=True)

            # Build screenshot filename: testname + timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name.replace("/", "_").replace(":", "_")
            screenshot_file = screenshots_dir / f"{test_name}_{timestamp}.png"

            # Capture full page screenshot
            page.screenshot(path=str(screenshot_file), full_page=True)

            # Print path to console for easy debugging
            print(f"\n📸 Screenshot captured: {screenshot_file}")

@pytest.fixture
def update_organization_data():
    """Load update organization test data."""
    return DataReader.load_yaml("testdata/update_organization.yaml")



import pytest
import yaml
import os

@pytest.fixture
def report_test_data():
    """Reads report data from the YAML file in root > testdata"""
    # Get the path to the root directory
    base_path = os.path.abspath(os.path.dirname(__file__))
    yaml_path = os.path.join(base_path, "testdata", "report_registration.yaml")
    
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    
    return data


@pytest.fixture
def new_organization_page(page):
    """Provides the NewOrganizationPage object to your tests"""
    return NewOrganizationPage(page)

@pytest.fixture
def new_organization_data():
    """Reads the YAML file and provides the data dictionary"""
    # Use an absolute path or join with the current file's directory
    path = os.path.join(os.path.dirname(__file__), "testdata", "new_organization.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)