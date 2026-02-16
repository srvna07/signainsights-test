from playwright.sync_api import Page, expect
from .base_page import BasePage


class LoginPage(BasePage):
    """Login page object — Playwright best practices."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input           = page.get_by_label("Username")
        self.password_input           = page.get_by_label("Password")
        self.login_button             = page.get_by_role("button", name="Login")
        self.welcome_text             = page.get_by_text("Welcome back")
        self.error_message            = page.get_by_role("alert")
        self.forgot_password_link     = page.get_by_text("Forgot Password?")

        # Validation errors
        self.username_required_error  = page.get_by_text("Username is required")
        self.password_required_error  = page.get_by_text("Password is required")
        self.password_incorrect_error = page.get_by_text("Password is incorrect")

        # FIX #3: was h5.MuiTypography-h5 CSS class — fragile, breaks on MUI upgrades.
        # Use semantic heading role instead — resilient to any style change.
        self.forgot_password_header   = page.get_by_role("heading", name="Forgot Password")

    # ── Navigation ───────────────────────────────────────────────────────────
    def navigate(self, base_url: str):
        """Navigate to login page."""
        self.navigate_to(base_url)

    # ── Actions ──────────────────────────────────────────────────────────────
    def login(self, username: str, password: str):
        """Fill credentials and submit."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def click_forgot_password(self):
        self.forgot_password_link.click()

    # ── Assertions (web-first — all auto-retry) ──────────────────────────────
    def verify_page_loaded(self):
        """Verify login page elements are visible."""
        expect(self.welcome_text).to_be_visible()
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()

    def verify_error_message_visible(self):
        expect(self.error_message).to_be_visible()

    def verify_error_message_hidden(self):
        expect(self.error_message).not_to_be_visible()
