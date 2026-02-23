from time import sleep
from playwright.sync_api import Page, expect
from .base_page import BasePage
from .login_page import LoginPage


class UserTypeAccessPage(BasePage):
    """
    Page object covering role-based access verification.

    Roles tested:
        - Super Admin
        - Signa User
        - Organization Admin
        - Organization User
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Navigation / Sidebar ──────────────────────────────────────────
        self.user_management_btn = page.get_by_role("button", name=" User Management")
        self.report_registration_btn = page.get_by_role("button", name=" Report Registration")
        self.org_registration_btn = page.get_by_role("button", name=" Organizations")
        self.new_user_btn = page.get_by_role("button", name="New User")

        # ── User Table / Search ───────────────────────────────────────────
        self.search_input = page.get_by_role("textbox", name="Search")

        # ── Form Fields ───────────────────────────────────────────────────
        self.first_name = page.get_by_role("textbox", name="First Name")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.username_field = page.get_by_role("textbox", name="User Name")
        self.email = page.get_by_role("textbox", name="Email")

        # ── Dropdowns ─────────────────────────────────────────────────────
        self.role_dropdown = page.get_by_role("combobox", name="Role")
        self.organization_dropdown = page.get_by_role("combobox", name="Organization", exact=True)
        self.user_type_dropdown = page.get_by_role("combobox", name="User Type")

        # ── Action Buttons ────────────────────────────────────────────────
        self.create_btn = page.get_by_role("button", name="Create")
        self.update_btn = page.get_by_role("button", name="Update")
        self.delete_btn = page.get_by_role("button", name="Delete")

        # ── Toast / Alert Messages ────────────────────────────────────────
        self.success_message = page.get_by_text("User created successfully")
        self.delete_success_message = page.get_by_text("User deleted successfully")

    # ─────────────────────────────────────────────────────────────────────
    # Login — all login logic lives here, not in conftest
    # ─────────────────────────────────────────────────────────────────────

    def login_as(self, base_url: str, username: str, password: str):
        """Navigate to login page, log in, wait for dashboard."""
        login = LoginPage(self.page)
        login.navigate(base_url)
        login.login(username, password)
        self.page.wait_for_url("**/dashboard**", timeout=15000)

    # ─────────────────────────────────────────────────────────────────────
    # Navigation
    # ─────────────────────────────────────────────────────────────────────

    def navigate_to_dashboard(self):
        from utils.data_reader import DataReader
        from utils.env_loader import load_env
        config = DataReader.load_yaml(f"configs/{load_env()}.yaml")
        self.page.goto(f"{config['base_url'].rstrip('/')}/dashboard")
        self.page.wait_for_load_state("networkidle")

    def open_user_management(self):
        self.user_management_btn.click()

    def open_report_registration(self):
        self.report_registration_btn.click()

    def open_org_registration(self):
        self.org_registration_btn.click()

    # ─────────────────────────────────────────────────────────────────────
    # Sidebar Assertions
    # ─────────────────────────────────────────────────────────────────────

    def assert_user_management_visible(self):
        expect(self.user_management_btn).to_be_visible()

    def assert_report_registration_visible(self):
        expect(self.report_registration_btn).to_be_visible()

    def assert_report_registration_hidden(self):
        expect(self.report_registration_btn).not_to_be_visible()

    def assert_org_registration_visible(self):
        expect(self.org_registration_btn).to_be_visible()

    def assert_org_registration_hidden(self):
        expect(self.org_registration_btn).not_to_be_visible()

    # ─────────────────────────────────────────────────────────────────────
    # User Type Dropdown Assertions
    # ─────────────────────────────────────────────────────────────────────

    def assert_user_type_option_present(self, option: str):
        self.user_type_dropdown.click()
        sleep(0.3)
        expect(self.page.get_by_role("option", name=option, exact=True)).to_be_visible()
        self.page.keyboard.press("Escape")

    def assert_user_type_option_absent(self, option: str):
        self.user_type_dropdown.click()
        sleep(0.3)
        expect(self.page.get_by_role("option", name=option, exact=True)).not_to_be_visible()
        self.page.keyboard.press("Escape")

    # ─────────────────────────────────────────────────────────────────────
    # User Table Assertions
    # ─────────────────────────────────────────────────────────────────────

    def search_user(self, username: str):
        self.search_input.click()
        self.search_input.fill(username)
        sleep(0.8)

    def assert_user_visible_in_table(self, username: str):
        self.search_user(username)
        expect(self.page.get_by_role("cell", name=username, exact=True)).to_be_visible()

    def assert_user_not_visible_in_table(self, username: str):
        self.search_user(username)
        expect(self.page.get_by_role("cell", name=username, exact=True)).not_to_be_visible()

    def assert_edit_button_visible_for(self, username: str):
        self.search_user(username)
        expect(self.page.get_by_role("button", name="Edit").first).to_be_visible()

    def assert_edit_button_hidden_for(self, username: str):
        self.search_user(username)
        expect(self.page.get_by_role("button", name="Edit").first).not_to_be_visible()

    def assert_delete_button_visible_for(self, username: str):
        self.search_user(username)
        expect(self.page.get_by_role("button", name="Delete").first).to_be_visible()

    def assert_delete_button_hidden_for(self, username: str):
        self.search_user(username)
        expect(self.page.get_by_role("button", name="Delete").first).not_to_be_visible()

    # ─────────────────────────────────────────────────────────────────────
    # Create User
    # ─────────────────────────────────────────────────────────────────────

    def fill_minimal_user_form(self, first: str, last: str, username: str,
                               email: str, user_type: str, role: str, org: str):
        """
        Fill the New User form.
        Order: User Type → Role → Organization (org is disabled until user type is set).
        """
        self.new_user_btn.click()
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.username_field.fill(username)
        self.email.fill(email)

        # 1. User Type first
        self.user_type_dropdown.click()
        self.page.get_by_role("option", name=user_type, exact=True).click()

        # 2. Role
        self.role_dropdown.click()
        self.page.get_by_role("option", name=role, exact=True).click()

        # 3. Organization — wait for it to enable after User Type is selected
        expect(self.organization_dropdown).to_be_enabled()
        self.organization_dropdown.click()
        self.page.get_by_role("option", name=org, exact=True).click()

    def submit_and_verify_created(self, track_in: dict = None, username: str = None):
        """
        Submit form and verify success toast.
        Registers username in track_in['created_usernames'] for teardown cleanup.
        """
        self.create_btn.click()
        expect(self.success_message).to_be_visible()
        if track_in is not None and username:
            track_in.setdefault("created_usernames", []).append(username)

    # ─────────────────────────────────────────────────────────────────────
    # Delete User — used by teardown cleanup in conftest
    # ─────────────────────────────────────────────────────────────────────

    def delete_user_by_username(self, username: str):
        """Search, click Delete, confirm — used for post-test cleanup."""
        self.search_user(username)
        self.page.get_by_role("button", name="Delete").first.click()
        self.page.get_by_role("button", name="Delete").first.click()  # confirm
        expect(self.delete_success_message).to_be_visible()