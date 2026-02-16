import re
from playwright.sync_api import Page, expect
from .base_page import BasePage


class LandingPage(BasePage):
    """Landing / Dashboard page object — Playwright best practices."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Top bar
        self.user_menu_button = page.get_by_role("button", name="Signed in as Test User")

        # User menu dropdown
        self.logout_menu_item      = page.get_by_role("menuitem", name="Logout")
        self.logout_confirm_button = page.get_by_role("button", name="Logout")

        # FIX #4: was get_by_role("button", name=" Dashboard") with a leading
        # icon-font character prefix. exact=False matches on readable text only,
        # so icon character changes never break the locator.
        self.nav_dashboard            = page.get_by_role("button", name="Dashboard",            exact=False)
        self.nav_user_management      = page.get_by_role("button", name="User Management",      exact=False)
        self.nav_insights             = page.get_by_role("button", name="Insights",             exact=False)
        self.nav_organizations        = page.get_by_role("button", name="Organizations",        exact=False)
        self.nav_report_registrations = page.get_by_role("button", name="Report Registrations", exact=False)

        # Footer
        self.privacy_policy_link = page.get_by_role("link", name="Privacy Policy")
        self.terms_link          = page.get_by_role("link", name="Terms & Conditions")

    # ── Navigation ───────────────────────────────────────────────────────────
    def navigate(self, base_url: str):
        """Navigate directly to the dashboard."""
        self.navigate_to(f"{base_url.rstrip('/')}/dashboard")

    # ── Actions ──────────────────────────────────────────────────────────────
    def click_sidebar_item(self, name: str):
        """Click a sidebar button by visible text. exact=False ignores icon prefix."""
        self.page.get_by_role("button", name=name, exact=False).click()

    def click_user_menu(self):
        self.user_menu_button.click()

    def click_logout(self):
        self.click_user_menu()
        self.logout_menu_item.click()
        self.logout_confirm_button.click()

    def click_privacy_policy(self):
        self.privacy_policy_link.click()

    def click_terms(self):
        self.terms_link.click()

    # ── Assertions (web-first — all auto-retry) ──────────────────────────────
    def verify_page_loaded(self):
        """Verify all key landing page elements are visible.

        FIX #1: was using pytest_check + is_visible() — point-in-time boolean
        checks with no retry (Selenium pattern). Now uses expect() which
        auto-retries until visible or timeout — the correct Playwright pattern.
        """
        expect(self.user_menu_button).to_be_visible()
        expect(self.nav_dashboard).to_be_visible()
        expect(self.nav_user_management).to_be_visible()
        expect(self.nav_insights).to_be_visible()
        expect(self.nav_organizations).to_be_visible()
        expect(self.nav_report_registrations).to_be_visible()
        expect(self.privacy_policy_link).to_be_visible()
        expect(self.terms_link).to_be_visible()

    def verify_url_contains(self, text: str):
        """Verify URL contains specified text — delegates to BasePage helper."""
        self.assert_url_contains(text)
