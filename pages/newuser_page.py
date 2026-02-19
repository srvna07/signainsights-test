from time import sleep

from playwright.sync_api import Page, expect
from .base_page import BasePage


class NewUserPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # -----------------------------
        # Buttons
        # -----------------------------
        self.user_management_btn = page.get_by_role("button", name=" User Management")
        self.new_user_btn = page.get_by_role("button", name="New User")
        self.create_btn = page.get_by_role("button", name="Create")
        self.delete_btn = page.get_by_role("button", name="Delete")


        # -----------------------------
        # Textboxes
        # -----------------------------
        self.first_name = page.get_by_role("textbox", name="First Name")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.username = page.get_by_role("textbox", name="User Name")
        self.email = page.get_by_role("textbox", name="Email")
        self.dob = page.get_by_role("textbox", name="Date of Birth")
        self.phone = page.get_by_role("textbox", name="1 (702) 123-")  # placeholder dynamic, adjust if needed
        self.address1 = page.get_by_role("textbox", name="Address1")
        self.address2 = page.get_by_role("textbox", name="Address2")
        self.country = page.get_by_role("textbox", name="Country")
        self.city = page.get_by_role("textbox", name="City")
        self.state = page.get_by_role("textbox", name="State")
        self.zip_code = page.get_by_role("textbox", name="Zip Code")

        # -----------------------------
        # Search (User Management table)
        # -----------------------------
        self.search_input = page.get_by_role("textbox", name="Search")

        # -----------------------------
        # Dropdowns
        # -----------------------------
        self.role_dropdown = page.get_by_role("combobox", name="Role")
        self.organization_dropdown = page.get_by_role("combobox", name="Organization", exact=True)
        self.user_type_dropdown = page.get_by_role("combobox", name="User Type")
        self.secondary_org_dropdown = page.get_by_role("combobox", name="Secondary Organization")
        self.report_dropdown = page.get_by_role("combobox", name="Select Report")

        # -----------------------------
        # Success message
        # -----------------------------
        self.success_message = page.get_by_text("User created successfully")
        self.delete_success_message = page.get_by_text("User deleted successfully")

        self.update_btn = page.get_by_role("button", name="Update")
        self.update_success_message = page.get_by_text("User updated successfully")


    # -----------------------------
    # Methods
    # -----------------------------
    def open_form(self):
        self.user_management_btn.click()
        self.new_user_btn.click()

    def fill_basic_info(self, first, last, username, email):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.username.fill(username)
        self.email.fill(email)

    def select_role(self, role_name):
        self.role_dropdown.click()
        self.page.get_by_role("option", name=role_name).click()

    def select_organization(self, org_name):
        self.organization_dropdown.click()
        self.page.get_by_role("option", name=org_name).click()

    def select_user_type(self, user_type):
        self.user_type_dropdown.click()
        self.page.get_by_role("option", name=user_type).click()

    def select_secondary_orgs(self, *orgs):
        self.secondary_org_dropdown.click()
        for org in orgs:
            self.page.get_by_role("option", name=org).click()

    def fill_contact_info(self, dob, phone, address1, address2, country, city, state, zipCode):
        self.dob.fill(dob)
        self.phone.fill(phone)
        self.address1.fill(address1)
        self.address2.fill(address2)
        self.country.fill(country)
        self.city.fill(city)
        self.state.fill(state)
        self.zip_code.fill(zipCode)

    def select_reports(self, *reports):
        self.report_dropdown.click()
        for report in reports:
            self.page.get_by_role("option", name=report).click()

    def submit_form(self):
        self.create_btn.click()

    def verify_success(self):
        """Verify user creation success message is visible."""
        expect(self.success_message).to_be_visible()

# -----------------------------
    # Delete methods
    # -----------------------------
    def search_user(self, username: str):
        """Search for a user by username in the table."""
        self.search_input.click()
        self.search_input.fill(username)

    def verify_user_in_table(self, username: str):
        self.search_input.click()
        self.search_input.fill(username)
        expect(self.page.get_by_text(username, exact=False)).to_be_visible()

    def delete_user(self, username: str):
        """Full delete flow (from codegen):
        search → click Delete (trash icon) → click Delete (confirm dialog).
        """
        self.search_user(username)
        sleep(1)
        self.delete_btn.click()   # trash icon

        self.delete_btn.click()   # confirm dialog

    def verify_delete_success(self):
        """Verify the delete success toast is visible."""
        expect(self.delete_success_message).to_be_visible()

    def verify_user_not_in_table(self, username: str):
        """Verify the deleted user no longer appears in the table."""
        expect(self.page.get_by_role("cell", name=username, exact=True)).not_to_be_visible()

    def edit_user(self, username: str):
        """Search for user and click Edit icon."""
        self.search_user(username)
        sleep(1)
        self.page.get_by_role("button", name="Edit").first.click()

    def verify_update_success(self):
        """Verify update success toast is visible."""
        expect(self.update_success_message).to_be_visible()

    def navigate_to_dashboard(self):
        """Navigate to dashboard using base_url from config."""
        from utils.data_reader import DataReader
        from utils.env_loader import load_env

        config = DataReader.load_yaml(f"configs/{load_env()}.yaml")
        self.page.goto(f"{config['base_url'].rstrip('/')}/dashboard")

    def verify_user_updated(self, username: str, updated_first: str, updated_last: str, updated_role: str):
        """Verify user updates in table and by re-opening edit form."""
        # Verify changes in table (list page)
        self.verify_user_in_table(username)
        expect(self.page.get_by_text(updated_first, exact=False)).to_be_visible()
        expect(self.page.get_by_text(updated_last, exact=False)).to_be_visible()

        # Navigate to dashboard then back to User Management
        self.navigate_to_dashboard()
        self.user_management_btn.click()

        # Re-open the edit form and verify fields are persisted
        self.edit_user(username)
        expect(self.first_name).to_have_value(updated_first)
        expect(self.last_name).to_have_value(updated_last)
        expect(self.role_dropdown).to_have_value(updated_role)