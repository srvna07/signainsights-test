import os
import pytest
from pages.login_page import LoginPage
from utils.data_reader import DataReader
from utils.env_loader import load_env

# Load config for base_url
_config = DataReader.load_yaml(f"configs/{load_env()}.yaml")


# ── Override: login fresh before every test in this file ─────────────────────
@pytest.fixture
def authenticated_page(page):
    login = LoginPage(page)
    login.navigate(_config["base_url"])
    login.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))

    # Wait for URL to leave login page — confirms login succeeded
    page.wait_for_url(
        lambda url: "login" not in url,
        timeout=15000
    )

    # Navigate to dashboard and wait for sidebar to render
    page.goto(f"{_config['base_url'].rstrip('/')}/dashboard")
    page.wait_for_load_state("domcontentloaded")

    return page


# ── TC 01: Create new user ────────────────────────────────────────────────────
@pytest.mark.smoke
def test_create_new_user(authenticated_page, new_user_page, new_user_data):
    page = new_user_page

    user    = new_user_data["user"]
    contact = new_user_data["contact"]

    page.open_form()

    page.fill_basic_info(
        first    = user["firstName"],
        last     = user["lastName"],
        username = user["username"],
        email    = user["email"]
    )

    page.select_role(new_user_data["role"])
    page.select_organization(new_user_data["organization"])
    page.select_user_type(new_user_data["userType"])
    page.select_secondary_orgs(*new_user_data["secondaryOrganizations"])
    page.fill_contact_info(**contact)
    page.select_reports(*new_user_data["reports"])

    page.submit_form()
    page.verify_success()
