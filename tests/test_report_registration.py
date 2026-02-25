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

# organization_test_data = DataFactory
organization_test_data = DataGenerator.update_organization_fields()
data = TestDataLoader.import_report_registration_test_data()
org_data = TestDataLoader.import_new_organization_test_data()

@pytest.mark.smoke
def test_create_new_organization(authenticated_page, new_organization_page: NewOrganizationPage, new_organization_data):
    # 1. Get the data blocks from the fixture
    org_info = new_organization_data["organization"]
    contact_info = new_organization_data["contact"]

    # 2. Call the action (Simple and clean!)
    new_organization_page.create_organization_action(
        organization=org_info, 
        contact=contact_info
    )
    
    # 3. Verify success
    expect(authenticated_page.get_by_text(org_info["namePrefix"])).to_be_visible()

@pytest.mark.smoke
def test_create_new_report(authenticated_page, report_registration_page: ReportRegistrationPageActions, report_registration_data):
    # Use 'report_registration_data' for everything to stay consistent
    new_report = report_registration_data["new_report"]
    
    # FIX: Get organization name from the global org_data since it's loaded at the top
    # or from the merged fixture if you updated it as shown above
    org_name_prefix = org_data["organization"]["namePrefix"] 
    
    report_registration_page.create_new_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"],
        dataset_id=new_report["dataset_id"],
        organization=org_name_prefix
    )
    expect(authenticated_page.get_by_text(new_report["report_name"])).to_be_visible()

@pytest.mark.smoke
def test_edit_created_report(authenticated_page, report_registration_data, report_registration_page: ReportRegistrationPageActions):
    
    new_report = report_registration_data["new_report"]
    edit_report = report_registration_data["edit_report"]         

    report_registration_page.edit_created_report(new_report["report_name"], edit_report["report_name"])
    expect(authenticated_page.get_by_text(edit_report["report_name"])).to_be_visible()

@pytest.mark.smoke
def test_search_bar(authenticated_page, report_registration_page: ReportRegistrationPageActions, report_registration_data):
    # 1. Get the data
    edit_report = report_registration_data["edit_report"]
    report_name = edit_report["report_name"]

    # 2. Perform Search
    report_registration_page.Search_report(report_name)
    
    # 3. Verify Result
    report_registration_page.verify_search_bar_works(report_name)

    # 4. Clear The Search Bar
    report_registration_page.clear_search_bar()

@pytest.mark.smoke
def test_rows_per_page_5(authenticated_page, report_registration_page: ReportRegistrationPageActions):
    
    # 1. Change pagination
    report_registration_page.check_rows_per_pages_5()

    # 2. Assert
    rows = authenticated_page.locator("table tbody tr")
    expect(rows.first).to_be_visible() # Wait for table to load
    assert rows.count() <= 5

def test_rows_per_page_25(authenticated_page, report_registration_page: ReportRegistrationPageActions):
    
    # Assuming you'll add a check_rows_per_pages_25 method to your Actions class
    report_registration_page.click_row_per_page_dropdown()
    report_registration_page.click_row_per_page_count_25()

    rows = authenticated_page.locator("table tbody tr")
    assert rows.count() <= 25

def test_navigate_between_next_and_previous_pages(authenticated_page, report_registration_page: ReportRegistrationPageActions):
    
    # 1. Navigate to the registrations page first
    report_registration_page.navigate_to_report_registration()

    # 2. Get the initial state (e.g., the first report name)
    first_page_report = authenticated_page.locator("table tbody tr").first.text_content()

    # 3. Go to next page
    report_registration_page.click_pagination_go_to_next_page()
    
    # Assert: The first row should now be different
    next_page_report = authenticated_page.locator("table tbody tr").first
    expect(next_page_report).not_to_have_text(first_page_report)

    # 4. Go back to previous page
    report_registration_page.click_pagination_go_to_previous_page()

    # Assert: We should be back to the original report
    expect(authenticated_page.locator("table tbody tr").first).to_have_text(first_page_report)

def test_delete_report(authenticated_page, report_registration_page: ReportRegistrationPageActions, report_registration_data):

    edit_report = report_registration_data["edit_report"]
    report_registration_page.delete_the_created_or_edited_report(edit_report["report_name"])
    report_registration_page.verify_report_deleted(edit_report["report_name"]) 


def test_delete_organization(authenticated_page, new_organization_page: NewOrganizationPage):
    delete_organization = organization_test_data["organization"]
    org_name = delete_organization["namePrefix"]
    new_organization_page.navigate_to_organization()
    new_organization_page.delete_organization(org_name)
    new_organization_page.verify_delete_success()

