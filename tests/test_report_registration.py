from playwright.sync_api import expect
from pages.report_registration_page import ReportRegistrationPageActions
import pytest

# Use the fixture names that Pytest actually found in your session
# These are: authenticated_page, report_test_data

def test_create_new_report(authenticated_page, report_test_data):
    
    report_page = ReportRegistrationPageActions(authenticated_page)
    report_page.navigate_to_report_registration()
    
    new_report = report_test_data["new_report"]

    report_page.create_new_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"]
    )

    # 2. Use 'authenticated_page' for assertions
    expect(authenticated_page.get_by_text(new_report["report_name"])).to_be_visible()


def test_edit_created_report(authenticated_page, report_test_data):
    report_page = ReportRegistrationPageActions(authenticated_page)
    new_report = report_test_data["new_report"]
    edit_report = report_test_data["edit_report"]

    # Create first
    report_page.create_new_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"]
    )

    # Edit
    report_page.edit_created_report(edit_report["report_name"])
    expect(authenticated_page.get_by_text(edit_report["report_name"])).to_be_visible()


def test_rows_per_page_5(authenticated_page):
    report_page = ReportRegistrationPageActions(authenticated_page)
    
    # 1. ADD THIS: Navigate to the correct page first
    report_page.locators.sidebar_report_registration.click() 
    
    # 2. Change pagination
    report_page.check_rows_per_pages_5()

    # 3. Assert
    rows = authenticated_page.locator("table tbody tr")
    expect(rows.first).to_be_visible() # Wait for table to load
    assert rows.count() <= 5

def test_rows_per_page_25(authenticated_page):
    report_page = ReportRegistrationPageActions(authenticated_page)
    
    # Assuming you'll add a check_rows_per_pages_25 method to your Actions class
    report_page.click_row_per_page_dropdown()
    report_page.click_row_per_page_count_25()

    rows = authenticated_page.locator("table tbody tr")
    assert rows.count() <= 25