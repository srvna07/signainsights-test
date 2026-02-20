from time import sleep
from playwright.sync_api import Page, expect
from .base_page import BasePage


class NewUserPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Buttons
        self.user_management_btn = page.get_by_role("button", name=" User Management")
        self.new_user_btn = page.get_by_role("button", name="New User")
        self.create_btn = page.get_by_role("button", name="Create")
        self.update_btn = page.get_by_role("button", name="Update")
        self.delete_btn = page.get_by_role("button", name="Delete")

        # Form fields
        self.first_name = page.get_by_role("textbox", name="First Name")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.username = page.get_by_role("textbox", name="User Name")
        self.email = page.get_by_role("textbox", name="Email")
        self.dob = page.get_by_role("textbox", name="Date of Birth")
        self.phone = page.get_by_role("textbox", name="1 (702) 123-")
        self.address1 = page.get_by_role("textbox", name="Address1")
        self.address2 = page.get_by_role("textbox", name="Address2")
        self.country = page.get_by_role("textbox", name="Country")
        self.city = page.get_by_role("textbox", name="City")
        self.state = page.get_by_role("textbox", name="State")
        self.zip_code = page.get_by_role("textbox", name="Zip Code")
        self.search_input = page.get_by_role("textbox", name="Search")

        # Dropdowns
        self.role_dropdown = page.get_by_role("combobox", name="Role")
        self.organization_dropdown = page.get_by_role("combobox", name="Organization", exact=True)
        self.user_type_dropdown = page.get_by_role("combobox", name="User Type")
        self.secondary_org_dropdown = page.get_by_role("combobox", name="Secondary Organization")
        self.report_dropdown = page.get_by_role("combobox", name="Select Report")

        # Success messages
        self.success_message = page.get_by_text("User created successfully")
        self.update_success_message = page.get_by_text("User updated successfully")
        self.delete_success_message = page.get_by_text("User deleted successfully")

    # ── Create Flow ──────────────────────────────────────────────────────────
    def open_form(self):
        self.user_management_btn.click()
        self.new_user_btn.click()

    def fill_basic_info(self, first: str, last: str, username: str, email: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.username.fill(username)
        self.email.fill(email)

    def select_role(self, role_name: str):
        self.role_dropdown.click()
        self.page.get_by_role("option", name=role_name, exact=True).click()

    def select_organization(self, org_name: str):
        self.organization_dropdown.click()
        self.page.get_by_role("option", name=org_name, exact=True).click()

    def select_user_type(self, user_type: str):
        self.user_type_dropdown.click()
        self.page.get_by_role("option", name=user_type, exact=True).click()

    def select_secondary_orgs(self, *orgs: str):
        self.secondary_org_dropdown.click()
        for org in orgs:
            self.page.get_by_role("option", name=org, exact=True).click()

    def fill_contact_info(self, dob: str, phone: str, address1: str, address2: str,
                          country: str, city: str, state: str, zipCode: str):
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
        expect(self.success_message).to_be_visible()

    # ── Update Flow ──────────────────────────────────────────────────────────
    def clear_field(self, field):
        """Clear input field if it has content."""
        if field.input_value():
            field.clear()

    def _clear_multi_select(self, dropdown):
        """Clear all selected chips in a multi-select dropdown."""
        clear_btn = dropdown.locator("..").get_by_role("button", name="Clear")
        if clear_btn.count() > 0:
            clear_btn.first.click()

    def update_user(self, update_data: dict):
        """Fill all updatable fields from update_user.yaml."""
        basic = update_data["updated_basic"]
        contact = update_data["contact"]

        # Basic info
        self.clear_field(self.first_name)
        self.first_name.fill(basic["firstName"])
        self.clear_field(self.last_name)
        self.last_name.fill(basic["lastName"])

        # Dropdowns
        self.select_role(update_data["role"])
        self.select_organization(update_data["organization"])
        self.select_user_type(update_data["userType"])

        # Multi-selects (clear existing then add new)
        self._clear_multi_select(self.secondary_org_dropdown)
        self.select_secondary_orgs(*update_data["secondaryOrganizations"])

        # Contact info
        self.dob.fill(contact["dob"])
        self.phone.fill(contact["phone"])
        for field_name in ["address1", "address2", "country", "city", "state"]:
            field = getattr(self, field_name)
            self.clear_field(field)
            field.fill(contact[field_name])
        self.clear_field(self.zip_code)
        self.zip_code.fill(contact["zipCode"])

        # Reports
        self._clear_multi_select(self.report_dropdown)
        self.select_reports(*update_data["reports"])

    def verify_update_success(self):
        expect(self.update_success_message).to_be_visible()

    def verify_user_updated(self, username: str, update_data: dict):
        """Verify updates in table and by re-opening form."""
        basic = update_data["updated_basic"]
        contact = update_data["contact"]

        # Verify in table
        self.verify_user_in_table(username)
        expect(self.page.get_by_text(basic["firstName"], exact=False)).to_be_visible()
        expect(self.page.get_by_text(basic["lastName"], exact=False)).to_be_visible()

        # Navigate away and back to force reload
        self.navigate_to_dashboard()
        self.user_management_btn.click()

        # Re-open form and verify field values
        self.edit_user(username)
        expect(self.first_name).to_have_value(basic["firstName"])
        expect(self.last_name).to_have_value(basic["lastName"])
        expect(self.role_dropdown).to_have_value(update_data["role"])
        expect(self.organization_dropdown).to_have_value(update_data["organization"])
        expect(self.user_type_dropdown).to_have_value(update_data["userType"])

        # Verify multi-selects via chips
        for org in update_data["secondaryOrganizations"]:
            expect(self.page.locator(".MuiAutocomplete-tag", has_text=org)).to_be_visible()

        # Verify contact info
        # expect(self.dob).to_have_value(contact["dob"])
        expect(self.phone).to_have_value(contact["phone"])
        expect(self.address1).to_have_value(contact["address1"])
        expect(self.address2).to_have_value(contact["address2"])
        expect(self.country).to_have_value(contact["country"])
        expect(self.city).to_have_value(contact["city"])
        expect(self.state).to_have_value(contact["state"])
        expect(self.zip_code).to_have_value(contact["zipCode"])

    # ── Delete Flow ──────────────────────────────────────────────────────────
    def search_user(self, username: str):
        self.search_input.click()
        self.search_input.fill(username)

    def edit_user(self, username: str):
        self.search_user(username)
        sleep(1)
        self.page.get_by_role("button", name="Edit").first.click()

    def delete_user(self, username: str):
        self.search_user(username)
        sleep(1)
        self.delete_btn.click()  # trash icon
        self.delete_btn.click()  # confirm

    def verify_delete_success(self):
        expect(self.delete_success_message).to_be_visible()

    def verify_user_not_in_table(self, username: str):
        expect(self.page.get_by_role("cell", name=username, exact=True)).not_to_be_visible()

    # ── Helpers ──────────────────────────────────────────────────────────────
    def verify_user_in_table(self, username: str):
        self.search_input.click()
        self.search_input.fill(username)
        expect(self.page.get_by_text(username, exact=False)).to_be_visible()

    def navigate_to_dashboard(self):
        from utils.data_reader import DataReader
        from utils.env_loader import load_env
        config = DataReader.load_yaml(f"configs/{load_env()}.yaml")
        self.page.goto(f"{config['base_url'].rstrip('/')}/dashboard")