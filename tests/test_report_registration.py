from playwright.sync_api import expect
from pages.report_registration_page import ReportRegistrationPageActions
from pages.organizations_page import NewOrganizationPage
from utils.test_data_loader import TestDataLoader
import yaml
from pathlib import Path
import pytest
import logging

# 1. FIX: Define the logger so it stops crashing
logger = logging.getLogger(__name__)

data = TestDataLoader.import_report_registration_test_data()

@pytest.mark.smoke
def test_create_new_organization(authenticated_page):
    # 1. Load the data using your new class method
    data = TestDataLoader.import_report_registration_test_data()
    org_data = data["organization"]

    # 2. create the Page Object
    org_page = NewOrganizationPage(authenticated_page)

    # 3. Call the action to perform the task
    org_page.create_organization_action(**org_data)

    # 4. Verify the resuls
    org_page.verify_success()

@pytest.mark.smoke
def test_create_new_report(authenticated_page):
    
    # 1. Access your data blocks
    new_report = data["new_report"]
    org_name = data["organization"]
    
    # 2. Use the data in your actions
    report_page = ReportRegistrationPageActions(authenticated_page)
    report_page.create_new_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"],
        dataset_id=new_report["dataset_id"],
        organization=org_name["name"]
    )

    expect(authenticated_page.get_by_text(new_report["report_name"])).to_be_visible()

@pytest.mark.smoke
def test_edit_created_report(authenticated_page, report_test_data):
    report_page = ReportRegistrationPageActions(authenticated_page)
    new_report = report_test_data["new_report"]
    edit_report = report_test_data["edit_report"]

    # 2. FIX: Added the missing dataset_id and organization here
    report_page.create_new_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"],
        dataset_id=new_report["dataset_id"],
        organization="Default Org"          
    )

    report_page.edit_created_report(edit_report["report_name"])
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