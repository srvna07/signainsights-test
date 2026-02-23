import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from utils.env_loader import load_env
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.newuser_page import NewUserPage
from pages.landing_page import LandingPage
from pages.user_type_access_page import UserTypeAccessPage
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from pathlib import Path
from datetime import datetime

load_dotenv()

logger = get_logger(__name__)

ENV = load_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")


# ---------------------------
# Browser + Page Fixture
# ---------------------------
@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        browser = getattr(p, config["browser"]).launch(headless=config["headless"])
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
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
    return config


# ---------------------------
# Page Object Fixtures
# ---------------------------
@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def forgot_password_page(page):
    return ForgotPasswordPage(page)


@pytest.fixture
def landing_page(page):
    return LandingPage(page)


@pytest.fixture
def new_user_page(page):
    return NewUserPage(page)


@pytest.fixture
def update_user_data():
    return DataReader.load_yaml("testdata/update_user.yaml")


# ---------------------------
# Authenticated Session Fixture
# ---------------------------
@pytest.fixture(scope="session")
def authenticated_page(page):
    login = LoginPage(page)
    login.navigate(config["base_url"])
    login.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    page.wait_for_url("**/dashboard**", timeout=15000)
    logger.info("✓ Logged in (session-based authentication). Reusing page…")
    return page


@pytest.fixture(scope="session")
def new_user_data():
    data = DataReader.load_yaml("testdata/new_user.yaml")
    prefix = data["user"]["usernamePrefix"]
    domain = data["user"]["emailDomain"]
    data["user"]["username"] = DataFactory.random_username(prefix)
    data["user"]["email"] = DataFactory.random_email(prefix, domain)
    return data


# ---------------------------
# User Type Access — Data Fixtures
#
# create_users is a list — each entry gets a random username/email
# at session start so every test run uses unique credentials.
# created_usernames is attached for teardown cleanup.
# ---------------------------

def _inject_random_data(data: dict) -> dict:
    """Generate unique username + email for every entry in create_users list."""
    for user in data.get("create_users", []):
        user["username"] = DataFactory.random_username(user["usernamePrefix"])
        user["email"] = DataFactory.random_email(user["usernamePrefix"], user["emailDomain"])
    data["created_usernames"] = []
    return data


@pytest.fixture(scope="session")
def super_admin_data():
    return _inject_random_data(DataReader.load_yaml("testdata/user_types/super_admin.yaml"))


@pytest.fixture(scope="session")
def signa_user_data():
    return _inject_random_data(DataReader.load_yaml("testdata/user_types/signa_user.yaml"))


@pytest.fixture(scope="session")
def org_admin_data():
    return _inject_random_data(DataReader.load_yaml("testdata/user_types/org_admin.yaml"))


@pytest.fixture(scope="session")
def org_user_data():
    return DataReader.load_yaml("testdata/user_types/org_user.yaml")



# ---------------------------
# User Type Access — Role Page Fixtures
#
# scope="class" → login once per test class, not per test.
# Teardown deletes every user created during that class's tests.
# ---------------------------

def _cleanup_created_users(access: UserTypeAccessPage, data: dict):
    """Delete all users registered in data['created_usernames'] after class finishes."""
    usernames = data.get("created_usernames", [])
    if not usernames:
        return
    try:
        access.navigate_to_dashboard()
        access.open_user_management()
        for username in usernames:
            try:
                access.delete_user_by_username(username)
                logger.info(f"🗑  Deleted: {username}")
            except Exception as e:
                logger.warning(f"⚠  Could not delete '{username}': {e}")
    except Exception as e:
        logger.warning(f"⚠  Cleanup navigation failed: {e}")


@pytest.fixture(scope="class")
def super_admin_page(page, config_fixture, super_admin_data):
    access = UserTypeAccessPage(page)
    access.login_as(config_fixture["base_url"], os.getenv("SA_USERNAME"), os.getenv("SA_PASSWORD"))
    yield access
    _cleanup_created_users(access, super_admin_data)


@pytest.fixture(scope="class")
def signa_user_page(page, config_fixture, signa_user_data):
    access = UserTypeAccessPage(page)
    access.login_as(config_fixture["base_url"], os.getenv("SU_USERNAME"), os.getenv("SU_PASSWORD"))
    yield access
    _cleanup_created_users(access, signa_user_data)


@pytest.fixture(scope="class")
def org_admin_page(page, config_fixture, org_admin_data):
    access = UserTypeAccessPage(page)
    access.login_as(config_fixture["base_url"], os.getenv("OA_USERNAME"), os.getenv("OA_PASSWORD"))
    yield access
    _cleanup_created_users(access, org_admin_data)


@pytest.fixture(scope="class")
def org_user_page(page, config_fixture):
    access = UserTypeAccessPage(page)
    access.login_as(config_fixture["base_url"], os.getenv("OU_USERNAME"), os.getenv("OU_PASSWORD"))
    yield access


# ---------------------------
# Screenshot on Failure Hook
# ---------------------------
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
            test_name = item.name.replace("/", "_").replace(":", "_")
            screenshot_file = screenshots_dir / f"{test_name}_{timestamp}.png"
            page.screenshot(path=str(screenshot_file), full_page=True)
            print(f"\n📸 Screenshot captured: {screenshot_file}")
