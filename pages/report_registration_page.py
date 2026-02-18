from playwright.sync_api import Page, expect
from .base_page import BasePage

class ReportRegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        #module
        dialog = page.get_by_role("dialog")
        def row(self, report_name):
            return self.page.get_by_role("row", name=report_name)

        # Table
        self.new_report_bt = page.get_by_placeholder("Search")
        def preview_button(self, report_name):
            return self.row(report_name).get_by_role("button", name = "Preview")
        def edit_button(self, report_name):
            return self.row(report_name).get_by_role("button", name="Edit")
        def delete_button(self, report_name):
            return self.row(report_name).get_by_role("button", name="Delete")
        def specific_report(self, report_name):
            return self.row(report_name).get_by_role("row", name=report_name)

        #Pagination
        self.report_tabel_next_page = page.get_by_role("button", name="Go to next page")
        self.report_tabel_previous_page = page.get_by_role("button", name="Go to previous page")
        self.report_tabel_rows_per_page = page.get_by_role("combobox")
        self.report_table_10_rows_per_page = page.get_by_text("10")

        # Delete Confirmation dialogbox
        self.report_dialogbox_confirm_delete_button = dialog.get_by_role("button", name="delete")
        self.report_dialogbox_cancle_button = dialog.get_by_role("button", name="Cancel")

        
        


        




