from playwright.sync_api import Page, Locator
from .base_page import BasePage

class ReportRegistrationPageLocators(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # ---------- Static Page Elements ----------

        # Navigate report registration
        self.report_registrations_btn = page.get_by_role("button", name=" Report Registrations")

        # Search
        self.search_report = page.get_by_placeholder("Search")

        # New Report
        self.new_report = page.get_by_role("button", name = "New Report")

        # Pagination
        self.report_tabel_go_to_next_page = page.get_by_role("button", name = "Go to next page")
        self.report_tabel_go_to_previous_page = page.get_by_role("button", name = "Go to previous page")
        self.report_tabel_rows_per_page = page.get_by_role("combobox", name="Rows per page:")

        # Role Options
        self.admin_option_in_role_combobox = self.page.get_by_role("option", name = "Admin")
        self.hr_option_in_role_combobox = self.page.get_by_role("option", name = "HR")
        self.finance_option_in_role_combobox = self.page.get_by_role("option", name = "Finance")
        self.sales_and_marketing_option_in_role_combobox = self.page.get_by_role("option", name = "Sales & Marketing")
        self.operations_option_in_role_combobox = self.page.get_by_role("option", name = "Operations")

        # Row Per Page Options
        self.report_table_5_rows_per_page = page.get_by_role("option", name="5", exact=True)
        self.report_table_10_rows_per_page = page.get_by_role("option", name="10", exact=True)
        self.report_table_25_rows_per_page = page.get_by_role("option", name="25", exact=True)


    # ---------- Shared Dialog ----------
    def dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    # ---------- Dialog Buttons ----------
    def confirm_delete_button(self) -> Locator:
        return self.dialog().get_by_role("button", name = "Delete")

    def cancel_button(self) -> Locator:
        return self.dialog().get_by_role("button", name = "Cancel")

    def update_button(self) -> Locator:
        return self.dialog().get_by_role("button", name = "Update")
    
    def create_button(self) -> Locator:
        return self.dialog().get_by_role("button", name = "Create")

    # ---------- Dialog Inputs ----------
    def report_name_input(self) -> Locator:
        return self.dialog().get_by_label("Report Name *")

    def menu_input(self) -> Locator:
        return self.dialog().get_by_label("Menu *")

    def workspace_id_input(self) -> Locator:
        return self.dialog().get_by_label("WorkSpaceId *")

    def report_id_input(self) -> Locator:
        return self.dialog().get_by_label("ReportId *")

    def data_set_id_input(self) -> Locator:
        return self.dialog().get_by_label("DatasetId *")

    def dashboard_checkbox(self) -> Locator:
        return self.dialog().get_by_role("checkbox", name = "Do you want this report to be shown as a Dashboard?")

    # ---------- Combobox ----------
    def organization_combobox(self) -> Locator:
        return self.page.get_by_role("combobox", name = "Organization")

    def role_combobox(self) -> Locator:
        return self.page.get_by_role("combobox", name = "Role")

    def role_option(self, role_name: str) -> Locator:
        return self.page.get_by_role("option", name = role_name)

    def organization_option(self, organization: str) -> Locator:
        return self.page.get_by_role("option", name = organization)

    # ---------- Table ----------
    def row(self, report_name: str) -> Locator:
        return self.page.get_by_role("row", name = report_name)

    def preview_button(self, report_name: str) -> Locator:
        return self.row(report_name).get_by_role("button", name = "Preview")

    def edit_button(self, report_name: str) -> Locator:
        return self.row(report_name).get_by_role("button", name = "Edit")

    def delete_button(self, report_name: str) -> Locator:
        return self.row(report_name).get_by_role("button", name = "Delete")
    
    # --- Organization Combobox Option ------

    def organization_option(self, organization: str) -> Locator:
        return self.dialog().get_by_role("option", name = organization)
    
    # --- Search ------

    def search_input(self) -> Locator:
        return self.page.get_by_placeholder("Search")
    
    
class ReportRegistrationPageActions(BasePage):

    def __init__(self, page):
        self.page = page
        self.locators = ReportRegistrationPageLocators(page)

    def navigate_to_report_registration(self):
        self.locators.report_registrations_btn.click()
        self.locators.new_report.wait_for(state="visible")

    # Table
    def click_report_preview_button(self, report_name):
        self.locators.preview_button(report_name).click()

    def click_report_edit_button(self, report_name):
        self.locators.edit_button(report_name).click()

    def click_report_delete_button(self, report_name):
        self.locators.edit_button(report_name).click()
    
    # Edit dialog box
    def click_report_edit_confirmation_Button(self):
        self.locators.update_button().click()

    def click_report_edit_cancelation_button(self):
        self.locators.cancel_button().click()

    # Delete dialogbox
    def click_report_delete_confirmation_button(self):
        self.locators.confirm_delete_button().click()

    def click_report_delete_cancelation_button(self):
        self.locators.cancel_button().click()

    # Pagination
    def click_row_per_page_dropdown(self):
        self.locators.report_tabel_rows_per_page.click()

    def click_row_per_page_count_5(self):
        self.locators.report_table_5_rows_per_page.click()

    def click_row_per_page_count_10(self):
        self.locators.report_table_10_rows_per_page.click()

    def click_row_per_page_count_25(self):
        self.locators.report_table_25_rows_per_page.click()

    def click_pagination_go_to_next_page(self):
        self.locators.report_tabel_go_to_next_page.click()

    def click_pagination_go_to_next_page(self):
        self.locators.report_tabel_go_to_previous_page.click()
    
    # Search
    def Search_report(self, report_name):
        self.locators.search_report(report_name)

    # New Report
    def click_create_new_report(self):
        self.locators.new_report.click()

    def click_create_button(self):
        self.locators.create_button().click()

    # fill fields in create and edit report dialogbox
    def fill_the_report_name_file(self, report_name):
        self.locators.report_name_input().fill(report_name)

    def fill_the_menu_input(self, menu_name):
        self.locators.menu_input().fill(menu_name)

    def fill_workspace_id_input(self, workspace_id):
        self.locators.workspace_id_input().fill(workspace_id)

    def fill_report_id_input(self, report_id):
        self.locators.report_id_input().fill(report_id)

    def fill_dataset_id(self, data_set_id):
        self.locators.data_set_id_input().fill(data_set_id)

    def click_role_combobox(self):
        self.locators.role_combobox().click()

    def click_organization_combobox(self):
        self.locators.organization_combobox().click()

    def select_admin_role_in_role_combobox(self):
        self.locators.admin_option_in_role_combobox.click()

    def select_hr_role_in_role_combobox(self):
        self.locators.hr_option_in_role_combobox.click()

    def select_finance_role_in_role_combobox(self):
        self.locators.finance_option_in_role_combobox.click()

    def select_sales_and_marketing_role_in_role_combobox(self):
        self.locators.sales_and_marketing_option_in_role_combobox.click()

    def select_operations_role_in_role_combobox(self):
        self.locators.operations_option_in_role_combobox.click()

    def select_created_organization(self, organization):
        self.locators.organization_option(organization).click()



    def create_new_report(self, report_name, menu_name, workspace_id, report_id, dataset_id):
        self.click_create_new_report()
        self.fill_the_report_name_file(report_name)
        self.fill_the_menu_input(menu_name)
        self.fill_workspace_id_input(workspace_id)
        self.fill_report_id_input(report_id)
        self.fill_dataset_id(dataset_id)
        self.click_role_combobox()
        self.select_admin_role_in_role_combobox()
        self.select_hr_role_in_role_combobox()
        self.click_organization_combobox()
        self.select_created_organization()
        self.click_create_button()

    def edit_created_report(self, report_name):
        self.fill_the_report_name_file(report_name)
        self.click_role_combobox()
        self.select_sales_and_marketing_role_in_role_combobox()
        self.click_report_edit_confirmation_Button()

    def preview_report(self, report_name):
        self.click_report_preview_button(report_name)

    def check_rows_per_pages_5(self):
        self.click_row_per_page_dropdown()
        self.click_row_per_page_count_5()

    def check_rows_per_pages_10(self):
        self.click_row_per_page_dropdown()
        self.click_row_per_page_count_10()

    def navigate_between_next_and_previous_pages(self):
        self.click_pagination_go_to_next_page()
        self.click_report_preview_button()

    



    
        
    
