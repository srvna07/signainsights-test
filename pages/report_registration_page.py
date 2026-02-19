from playwright.sync_api import Page, expect
from .base_page import BasePage

class ReportRegistrationPageLocators(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page
        self.dialog: Locator = page.get_by_role("dialog")

        ### Static Locators ###

        # Module
        self.dialog = page.get_by_role("dialog")

        # Search
        self.search_report = page.get_by_placeholder("Search")

        # New report
        self.new_report = page.get_by_role("button", name = "New Report")
        
        # Pagination
        self.report_tabel_go_to_next_page = page.get_by_role("button", name="Go to next page")
        self.report_tabel_go_to_previous_page = page.get_by_role("button", name="Go to previous page")
        self.report_tabel_rows_per_page = page.get_by_role("combobox")
        self.report_table_5_rows_per_page = page.get_by_text("5")
        self.report_table_10_rows_per_page = page.get_by_text("10")
        self.report_table_25_rows_per_page = page.get_by_text("25")

        # Delete Confirmation dialogbox
        self.report_dialogbox_confirm_delete_button = self.dialog.get_by_role("button", name="delete")
        self.report_dialogbox_cancle_button = self.dialog.get_by_role("button", name="Cancel")

        # Create and Edit report Confirmation dialogbox
        self.dashboard_checkbox = self.dialog.get_by_role("checkbox",name="Do you want this report to be shown as a Dashboard?")
        self.organization_combobox = self.page.get_by_role("combobox", name="Organization")
        self.role_combobox = self.page.get_by_role("combobox", name="Role")
        self.admin_option_in_role_combobox = self.page.get_by_role("option", name = "Admin")
        self.hr_option_in_role_combobox = self.page.get_by_role("option", name = "HR")
        self.finance_option_in_role_combobox = self.page.get_by_role("option", name = "Finance")
        self.sales_and_marketing_option_in_role_combobox = self.page.get_by_role("option", name = "Sales & Marketing")
        self.operations_option_in_role_combobox = self.page.get_by_role("option", name = "Operations")

        self.report_dialogbox_edit_confirm_button = self.dialog.get_by_role("button", name="Update")
        self.report_dialogbox_edit_cancel_button = self.dialog.get_by_role("button", name="Cancel")
    
    ### Dynamic Locators ###
    def row(self, report_name):
        return self.page.get_by_role("row", name=report_name)
    
    # Table
    def preview_button(self, report_name):
        return self.row(report_name).get_by_role("button", name = "Preview")
    def edit_button(self, report_name):
        return self.row(report_name).get_by_role("button", name="Edit")
    def delete_button(self, report_name):
        return self.row(report_name).get_by_role("button", name="Delete")
    def specific_report(self, report_name):
        return self.row(report_name).get_by_role("row", name=report_name)
    
    # Create and Edit report Confirmation dialogbox
    def report_name_input(self):
        return self.dialog.get_by_label("Report Name *")
    def menu_input(self):
        return self.dialog.get_by_label("Menu *")
    def workspace_id_input(self):
        return self.dialog.get_by_label("WorkSpaceId *")
    def report_id_input(self):
        return self.dialog.get_by_label("ReportId *")
    def dataset_id_input(self):
        return self.dialog.get_by_label("DatasetId *")
    
    # Organization
    def select_specific_organization(self, organization):
        return self.dialog(organization).get_by_role("option", name=organization)
    

class ReportRegistrationPageActions(BasePage):

    def __init__(self, page):
        self.page = page
        self.locators = ReportRegistrationPageLocators(page)

    # Table
    def click_report_preview_button(self, report_name):
        self.locators.preview_button(report_name).click()

    def click_report_edit_button(self, report_name):
        self.locators.edit_button(report_name).click()

    def click_report_delete_button(self, report_name):
        self.locators.edit_button(report_name).click()
    
    # Edit dialog box
    def click_report_edit_confirmation_Button(self):
        self.locators.report_dialogbox_edit_confirm_button.click()

    def click_report_edit_cancelation_button(self):
        self.locators.report_dialogbox_edit_cancel_button.click()

    # Delete dialogbox
    def click_report_delete_confirmation_button(self):
        self.locators.report_dialogbox_confirm_delete_button.click()

    def click_report_delete_cancelation_button(self):
        self.locators.report_dialogbox_cancle_button.click()

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

    # fill fields in create and edit report dialogbox
    def fill_the_report_name_file(self, report_name):
        self.locators.report_name_input.fill(report_name)

    def fill_the_menu_input(self, menu_name):
        self.locators.menu_input.fill(menu_name)

    def fill_workspace_id_input(self, workspace_id):
        self.locators.workspace_id_input.fill(workspace_id)

    def fill_report_id_input(self, report_id):
        self.locators.report_id_input.fill(report_id)

    def click_role_combobox(self):
        self.locators.role_combobox.click()

    def click_organization_combobox(self):
        self.locators.organization_combobox.click()

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

    def 

    

    
