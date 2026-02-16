import re
from playwright.sync_api import Page, expect
from .base_page import BasePage


class ForgotPasswordPage(BasePage):
    """Forgot Password page object — Playwright best practices."""

    def __init__(self, page: Page):
        super().__init__(page)

        # FIX #3: was h5.MuiTypography-h5 CSS class — fragile, breaks on MUI upgrades.
        # Use semantic heading role — resilient to any style/version change.
        self.page_header            = page.get_by_role("heading", name="Forgot Password")

        self.email_input            = page.get_by_label("Email")
        self.send_reset_link_button = page.get_by_role("button", name="Send Reset Link")
        self.contact_us_button      = page.get_by_role("button", name="Contact Us")

        # Validation messages
        self.email_required_error   = page.get_by_text("Email is required")
        self.invalid_email_error    = page.get_by_text("User not found.")

        # Success alert
        self.success_message        = page.get_by_role("alert")

    # ── Navigation ───────────────────────────────────────────────────────────
    def navigate(self, base_url: str):
        """Navigate to the Forgot Password page."""
        self.navigate_to(f"{base_url.rstrip('/')}/forgot-password")

    # ── Actions ──────────────────────────────────────────────────────────────
    def fill_email(self, email: str):
        self.email_input.fill(email)

    def click_send_reset_link(self):
        self.send_reset_link_button.click()

    def submit_email(self, email: str):
        """Fill email and submit — combined helper."""
        self.fill_email(email)
        self.click_send_reset_link()

    def click_contact_us(self):
        self.contact_us_button.click()

    # ── Assertions (web-first — all auto-retry) ──────────────────────────────
    def verify_page_loaded(self):
        expect(self.page_header).to_be_visible()
        expect(self.email_input).to_be_visible()
        expect(self.send_reset_link_button).to_be_visible()

    def verify_header_text(self):
        expect(self.page_header).to_have_text("Forgot Password")

    def verify_email_required_error_visible(self):
        expect(self.email_required_error).to_be_visible()

    def verify_invalid_email_error_visible(self):
        expect(self.invalid_email_error).to_be_visible()

    def verify_success_message_visible(self):
        expect(self.success_message).to_be_visible()

    def verify_url(self, page):
        # FIX #5: was hardcoded "https://dev.signainsights.com/forgot-password"
        # Now uses regex fragment — works on any environment (dev, prod, staging).
        expect(page).to_have_url(re.compile(r"forgot-password"))
