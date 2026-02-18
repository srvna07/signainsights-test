from time import sleep

import pytest


# ── TC 01: Create new user ────────────────────────────────────────────────────
@pytest.mark.smoke
def test_create_new_user(authenticated_page, new_user_page, new_user_data):
    page = new_user_page

    user    = new_user_data["user"]
    contact = new_user_data["contact"]

    page.open_form()

    page.fill_basic_info(
        first    = user["firstName"],
        last     = user["lastName"],
        username = user["username"],
        email    = user["email"]
    )

    page.select_role(new_user_data["role"])
    page.select_organization(new_user_data["organization"])
    page.select_user_type(new_user_data["userType"])
    page.select_secondary_orgs(*new_user_data["secondaryOrganizations"])
    page.fill_contact_info(**contact)
    page.select_reports(*new_user_data["reports"])

    page.submit_form()
    page.verify_success()
    page.verify_user_in_table(user["username"])


# ── TC 02: Delete the created user ───────────────────────────────────────────
@pytest.mark.smoke
def test_delete_new_user(authenticated_page, new_user_page, new_user_data):
    """Search for the created user, delete via trash icon → confirm dialog,
    verify success message and user no longer appears in the table."""
    page     = new_user_page
    username = new_user_data["user"]["username"]

    # Navigate to User Management table
    page.user_management_btn.click()
    # page.page.wait_for_load_state("domcontentloaded")

    # Delete flow: search → trash icon → confirm Delete button
    page.delete_user(username)

    # Verify success toast
    page.verify_delete_success()

    # Verify user is gone from the table
    page.verify_user_not_in_table(username)
