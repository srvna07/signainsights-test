import pytest


# ── Create new organization ────────────────────────────────────────────────────
@pytest.mark.smoke
def test_create_new_organization(authenticated_page, new_organization_page, new_organization_data):
    page = new_organization_page

    org    = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    page.open_form()

    page.fill_basic_info(
        org_name=org["name"],
        franchise_id=org["franchise_id"]
    )

    
    page.fill_contact_info(**contact)
    

    page.submit_form()
    page.verify_success()



@pytest.mark.smoke
def test_create_org_with_existing_name(authenticated_page, new_organization_page, new_organization_data):
    """Attempt to create an organization with a name that already exists and verify error handling."""
    page = new_organization_page

    org_name = new_organization_data["organization"]["name"]
    contact = new_organization_data["contact"]

    page.open_form()

    page.fill_basic_info(
        org_name=org_name,  # Use the same name to trigger duplicate error
        franchise_id="FRAN123"
    )

    page.fill_contact_info(**contact)
    

    page.submit_form()

    # Verify that an error message about duplicate organization name is visible
    page.verify_duplicate_error()
    page.cancel_btn.click()  # Close the form


def test_edit_organization(authenticated_page, new_organization_page, new_organization_data,update_organization_data):
    """Edit the created organization's name and verify the update is successful."""
    page = new_organization_page

    org_name = new_organization_data["organization"]["name"]
    

    # Navigate to Organization Management table
    page.navigate_to_dashboard()
    page.organization_btn.click()
    

    # Edit flow: search → click Edit icon → change name → submit
    page.edit_organization(org_name)
    page.update_organization(update_organization_data)
    page.update_btn.click()

    # Verify success toast
    page.verify_update_success()

    # Verify the updated organization name appears in the table
    page.verify_organization_in_table(update_organization_data["updated_basic"]["name"])

# ── TC 02: Delete the created organization ───────────────────────────────────────────
@pytest.mark.smoke
def test_delete_new_organization(authenticated_page, new_organization_page, new_organization_data,update_organization_data):
    """Search for the created organization, delete via trash icon → confirm dialog,
    verify success message and organization no longer appears in the table."""
    page     = new_organization_page
    org_name = update_organization_data["updated_basic"]["name"]

    # Navigate to Organization Management table
    page.navigate_to_dashboard()
    page.organization_btn.click()
    

    # Delete flow: search → trash icon → confirm Delete button
    page.delete_organization(org_name)

    # Verify success toast
    page.verify_delete_success()

    # Verify organization is gone from the table
    page.verify_organization_not_in_table(org_name)