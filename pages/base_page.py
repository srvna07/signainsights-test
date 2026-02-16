import re
from playwright.sync_api import Page, expect


class BasePage:
    """
    Base class for all page objects.
    Provides shared navigation and assertion helpers so individual
    page objects don't duplicate the same boilerplate.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a URL and wait for DOM to be ready."""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def assert_url_contains(self, fragment: str):
        """Assert current URL contains fragment — auto-retrying via regex."""
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))

    def assert_url_exact(self, url: str):
        """Assert current URL matches exactly — auto-retrying."""
        expect(self.page).to_have_url(url)
