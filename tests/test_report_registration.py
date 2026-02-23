from playwright.sync_api import expect
from pages.report_registration_page import ReportRegistrationPageActions
from pages.organizations_page import NewOrganizationPage
from utils.testdata_loader import TestDataLoader
from utils.data_generator import DataGenerator
from utils.data_factory import DataFactory
import yaml
from pathlib import Path
import pytest
import logging

# 1. FIX: Define the logger so it stops crashing
logger = logging.getLogger(__name__)

# organization_test_data = DataFactory.
report_test_data = DataGenerator.update_report_fields()
organization_test_data = DataGenerator.update_organization_fields()
data = TestDataLoader.import_report_registration_test_data()
org_data = TestDataLoader.import_new_organization_test_data()


@pytest.mark.smoke
def test_create_new_organization(authenticated_page):
    # 1. Access the global data you loaded at the top
    org_info = org_data["organization"]
    contact_info = org_data["contact"]

    # 3. Initialize Page Object
    org_page = NewOrganizationPage(authenticated_page)
    org_name = org_info["namePrefix"]

    # 4. Call action (Now organization has both 'org_name' and 'franchise_id')
    org_page.create_organization_action(
        organization=org_info, 
        contact=contact_info
    )
    
@pytest.mark.smoke
def test_create_new_report(authenticated_page):
    
    # 1. Access your data blocks
    new_report = data["new_report"]
    org_name = org_data["organization"]
    
    # 2. Use the data in your actions
    report_page = ReportRegistrationPageActions(authenticated_page)
    report_page.create_new_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"],
        dataset_id=new_report["dataset_id"],
        organization=org_name["namePrefix"]
    )

    expect(authenticated_page.get_by_text(new_report["report_name"])).to_be_visible()

@pytest.mark.smoke
def test_edit_created_report(authenticated_page, report_test_data):
    report_page = ReportRegistrationPageActions(authenticated_page)
    new_report = report_test_data["new_report"]
    edit_report = report_test_data["edit_report"]         

    report_page.edit_created_report(new_report["report_name"], edit_report["report_name"])
    expect(authenticated_page.get_by_text(edit_report["report_name"])).to_be_visible()

@pytest.mark.smoke
def test_rows_per_page_5(authenticated_page):
    report_page = ReportRegistrationPageActions(authenticated_page)
    
    report_page.locators.report_registrations_btn.click() 
    
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

def test_navigate_between_next_and_previous_pages(authenticated_page):
    report_page = ReportRegistrationPageActions(authenticated_page)
    
    # 1. Navigate to the registrations page first
    report_page.navigate_to_report_registration()

    # 2. Get the initial state (e.g., the first report name)
    first_page_report = authenticated_page.locator("table tbody tr").first.text_content()

    # 3. Go to next page
    report_page.click_pagination_go_to_next_page()
    
    # Assert: The first row should now be different
    next_page_report = authenticated_page.locator("table tbody tr").first
    expect(next_page_report).not_to_have_text(first_page_report)

    # 4. Go back to previous page
    report_page.click_pagination_go_to_previous_page()

    # Assert: We should be back to the original report
    expect(authenticated_page.locator("table tbody tr").first).to_have_text(first_page_report)