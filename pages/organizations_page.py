from time import sleep

from playwright.sync_api import Page, expect
from .base_page import BasePage


class NewOrganizationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # -----------------------------
        # Buttons
        # -----------------------------
        self.organization_btn = page.get_by_role("button", name=" Organizations")
        self.new_organization__btn = page.get_by_role("button", name="New Organization")
        self.create_btn = page.get_by_role("button", name="Create")
        self.cancel_btn = page.get_by_role("button", name="Cancel")
        self.delete_btn = page.get_by_role("button", name="Delete")
        self.edit_btn = page.get_by_role("button", name="Edit")
        self.update_btn = page.get_by_role("button", name="Update")


        # -----------------------------
        # Textboxes
        # -----------------------------
        self.organization_name = page.get_by_role("textbox", name="Organization Name")
        self.franchise_id = page.get_by_role("textbox", name="Franchise ID")
        self.address_1 = page.get_by_role("textbox", name="Address 1")
        self.address_2 = page.get_by_role("textbox", name="Address 2")
        self.city = page.get_by_role("textbox", name="City")
        self.state = page.get_by_role("textbox", name="State")  # placeholder dynamic, adjust if needed
        self.country = page.get_by_role("textbox", name="Country")
        self.zip_code = page.get_by_role("textbox", name="Zip Code")
        self.phone = page.locator("text=Phone Number").locator("..").locator("input[type='tel']")
        self.mobile = page.locator("text=Mobile Number").locator("..").locator("input[type='tel']")
        self.web_address = page.get_by_role("textbox", name="Web Address")




        # -----------------------------
        # Search (User Management table)
        # -----------------------------
        self.search_input = page.get_by_role("textbox", name="Search")

        # -----------------------------
        # Success message
        # -----------------------------
        self.success_message = page.get_by_text("Organization created successfully")
        self.delete_success_message = page.get_by_text("Organization deleted successfully")
        self.update_success_message = page.get_by_text("Organization updated successfully")
        self.duplicate_error_message = page.get_by_text("Organization already exists.")

    # -----------------------------
    # Methods
    # -----------------------------
    def open_form(self):
        self.organization_btn.click()
        self.new_organization__btn.click()


    def fill_basic_info(self, org_name, franchise_id):
        self.organization_name.fill(org_name)
        self.franchise_id.fill(franchise_id)

        

    def fill_contact_info(self, phone, mobile,address1, address2, city, state, country, zip_code, web_address):
        self.phone.fill(phone)
        self.mobile.fill(mobile)
        self.address_1.fill(address1)
        self.address_2.fill(address2)
        self.city.fill(city)
        self.state.fill(state)
        self.country.fill(country)
        self.zip_code.fill(zip_code)
        self.web_address.fill(web_address)

    def submit_form(self):
        self.create_btn.click()

    def verify_success(self):
        """Verify user creation success message is visible."""
        expect(self.success_message).to_be_visible()

    # -----------------------------
    # Delete methods
    # -----------------------------
    def search_organization(self, org_name):
        """Search for an organization by name."""
        self.search_input.click()
        self.search_input.fill(org_name)

    def delete_organization(self, org_name):
        """Delete an organization by name."""
        self.search_organization(org_name)
        sleep(1)
        self.delete_btn.click()   # trash icon

        self.delete_btn.click()   # confirm dialog

    def verify_delete_success(self):
        """Verify the delete success toast is visible."""
        expect(self.delete_success_message).to_be_visible()

    

    def verify_organization_in_table(self, org_name: str):
        """Verify the organization appears in the table after creation or update."""
        self.search_organization(org_name)
        sleep(1)
        expect(self.page.get_by_text(org_name)).to_be_visible()


    def verify_duplicate_error(self):
        """Verify that the duplicate organization error message is visible."""
        expect(self.duplicate_error_message).to_be_visible()

    def verify_organization_not_in_table(self, org_name: str):
        """Verify the deleted organization no longer appears in the table."""
        self.search_organization(org_name)
        sleep(1)
        expect(self.page.get_by_text(org_name)).not_to_be_visible()


    # ── Update Flow ──────────────────────────────────────────────────────────
    def clear_field(self, field):
        """Clear input field if it has content."""
        if field.input_value():
            field.clear()

    def update_organization(self, update_data: dict):
        """Fill all updatable fields from update_organization.yaml."""
        basic = update_data["updated_basic"]
        contact = update_data["contact"]
        self.clear_field(self.organization_name)
        self.organization_name.fill(basic["name"])
        self.clear_field(self.franchise_id)
        self.franchise_id.fill(basic["franchise_id"])
        self.clear_field(self.phone)
        self.phone.fill(contact["phone"])
        self.clear_field(self.mobile)
        self.mobile.fill(contact["mobile"])
        self.clear_field(self.address_1)
        self.address_1.fill(contact["address1"])
        self.clear_field(self.address_2)
        self.address_2.fill(contact["address2"])
        self.clear_field(self.city)
        self.city.fill(contact["city"])
        self.clear_field(self.state)
        self.state.fill(contact["state"])
        self.clear_field(self.country)
        self.country.fill(contact["country"])
        self.clear_field(self.web_address)
        self.web_address.fill(contact["web_address"])
        self.clear_field(self.zip_code)
        self.zip_code.fill(contact["zip_code"])

    def verify_update_success(self):
        """Verify the update success toast is visible."""
        expect(self.update_success_message).to_be_visible()
    
    def verify_organization_updated(self, org_name: str, update_data: dict):
        """Verify updates in table and by re-opening form."""
        basic = update_data["updated_basic"]
        contact = update_data["contact"]

         # Verify in table
        self.verify_organization_in_table(org_name)
        expect(self.page.get_by_text(basic["name"], exact=False)).to_be_visible()
        

        # Navigate away and back to force reload
        self.navigate_to_dashboard()
        self.organizations_btn.click()

        # Re-open form and verify field values
        self.edit_organization(org_name)
        expect(self.organization_name).to_have_value(basic["name"])
        
        expect(self.franchise_id).to_have_value(basic["franchise_id"])
        
        
        # Verify contact info
        
        expect(self.phone).to_have_value(contact["phone"])
        expect(self.mobile).to_have_value(contact["mobile"])
        expect(self.address1).to_have_value(contact["address1"])
        expect(self.address2).to_have_value(contact["address2"])
        expect(self.country).to_have_value(contact["country"])
        expect(self.city).to_have_value(contact["city"])
        expect(self.state).to_have_value(contact["state"])
        expect(self.web_address).to_have_value(contact["web_address"])
        expect(self.zip_code).to_have_value(contact["zip_code"])

    def navigate_to_dashboard(self):
        from utils.data_reader import DataReader
        from utils.env_loader import load_env
        config = DataReader.load_yaml(f"configs/{load_env()}.yaml")
        self.page.goto(f"{config['base_url'].rstrip('/')}/dashboard")

    def search_organization(self, org_name: str):
        self.search_input.click()
        self.search_input.fill(org_name)

    def edit_organization(self, org_name: str):
        self.search_organization(org_name)
        sleep(1)
        self.page.get_by_role("button", name="Edit").first.click()

    def delete_organization(self, org_name: str):
        self.search_organization(org_name)
        sleep(1)
        self.delete_btn.click()  # trash icon
        self.delete_btn.click()  # confirm