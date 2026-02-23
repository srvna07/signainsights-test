import pytest
import uuid



# =========================================================
# FIXTURE 1 — Create 3 Organizations
# =========================================================
@pytest.fixture
def created_orgs(authenticated_page, new_organization_page, new_organization_data):
    base_org = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    
    orgs = []

    for i in range(3):
        unique = uuid.uuid4().hex[:4]
        org_name = f"{base_org['name']}_{i}_{unique}"
        franchise_id = f"{base_org['franchise_id']}_{i}_{unique}"

        new_organization_page.open_form()
        new_organization_page.fill_basic_info(org_name, franchise_id)
        new_organization_page.fill_contact_info(**contact)
        new_organization_page.submit_form()
        new_organization_page.verify_success()

        orgs.append(org_name)

    return orgs

# =========================================================
# FIXTURE 2 — Create 1 Report Per Organization
# =========================================================
@pytest.fixture
def created_reports(
    authenticated_page,
    report_registration_page,
    import_report_test_data,
    created_orgs
):

    report_map = {}
    base_data = import_report_test_data["new_report"]
    report_registration_page.navigate_to_report_registration()

    for i, org_name in enumerate(created_orgs):
        unique = uuid.uuid4().hex[:4]

        report_name = f"{base_data['report_name']}_{i}_{unique}"
        menu_name = f"{base_data['menu_name']}_{i}_{unique}"
        workspace_id = f"{base_data['work_space_id']}_{i}_{unique}"
        report_id = f"{base_data['report_id']}_{i}_{unique}"
        dataset_id = f"{base_data['data_set_id']}_{i}_{unique}"

        report_registration_page.create_new_report_with_organization(
            report_name=report_name,
            menu_name=menu_name,
            workspace_id=workspace_id,
            report_id=report_id,
            dataset_id=dataset_id,
            organization=org_name
        )

        report_map[org_name] = report_name

    return report_map

# =========================================================
# FINAL TEST
# =========================================================
@pytest.mark.smoke
def test_admin_access_and_report_visibility(
    authenticated_page,
    new_user_page,
    new_user_data,
    created_orgs,
    created_reports
):
    page = new_user_page
    user = new_user_data["user"]
    contact = new_user_data["contact"]
    page.navigate_to_dashboard()
    page.user_management_btn.click()

    org1, org2, org3 = created_orgs
    report1 = created_reports[org1]
    report2 = created_reports[org2]
    report3 = created_reports[org3]

# =====================================================
# ADMIN 1 → Org1 + Org2
# =====================================================
    username1 = f"{user['usernamePrefix']}{uuid.uuid4().hex[:6]}"
    email1 = f"{username1}{new_user_data['user']['emailDomain']}"

    page.open_form()
    page.fill_basic_info("Admin", "One", username1, email1)
    page.select_role("Admin")
    page.select_organization(org1)
    page.select_user_type("Organization Admin")
    page.select_secondary_orgs(org2)
    page.fill_contact_info(**contact)

#====================================================
# VERIFY REPORT VISIBILITY BEFORE ASSIGNING
#===================================================
    page.open_reports_dropdown()
    page.verify_report_visible(report1)
    page.verify_report_visible(report2)
    page.verify_report_not_visible(report3)
    page.close_reports_dropdown()

    # Assign Reports
    page.select_reports(report1, report2)
    


    page.submit_form()
    page.verify_success()


# =====================================================
# ADMIN 2 → Org1 + Org3
# =====================================================
    username2 = f"{user['usernamePrefix']}{uuid.uuid4().hex[:6]}"
    email2 = f"{username2}{new_user_data['user']['emailDomain']}"

    page.open_form()
    page.fill_basic_info("Admin", "Two", username2, email2)
    page.select_role("Admin")
    page.select_organization(org1)
    page.select_user_type("Organization Admin")
    page.select_secondary_orgs(org3)
    page.fill_contact_info(**contact)

    page.open_reports_dropdown()
    page.verify_report_visible(report1)
    page.verify_report_visible(report3)
    page.verify_report_not_visible(report2)
    page.close_reports_dropdown()

    # Assign Reports
    page.select_reports(report1, report3)

    page.submit_form()
    page.verify_success()

# =====================================================
# COMMON USER WITH MULTIPLE ORGS
# =====================================================
    username_common = f"{user['usernamePrefix']}{uuid.uuid4().hex[:6]}"
    email_common = f"{username_common}{new_user_data['user']['emailDomain']}"

    page.open_form()
    page.fill_basic_info("Common", "User", username_common, email_common)

    page.select_role("Admin")

    # Primary Org
    page.select_organization(org1)

    page.select_user_type("Organization User")

    # Secondary Orgs
    page.select_secondary_orgs(org2, org3)

    page.fill_contact_info(**contact)

    page.open_reports_dropdown()
    page.verify_report_visible(report1)
    page.verify_report_visible(report2)
    page.verify_report_visible(report3)
    page.close_reports_dropdown()
    # Assign all reports
    page.select_reports(report1, report2, report3)

    page.submit_form()
    page.verify_success()

