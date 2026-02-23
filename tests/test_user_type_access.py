"""
test_user_type_access.py

Tests the permission matrix for all four user types:
  - Super Admin
  - Signa User
  - Organization Admin
  - Organization User

Run with:
    pytest tests/test_user_type_access.py -m role_access -v
"""

import pytest
from playwright.sync_api import expect

#
# ══════════════════════════════════════════════════════════════════════════════
# TC-SA: Super Admin
# ══════════════════════════════════════════════════════════════════════════════
#
# @pytest.mark.smoke
# @pytest.mark.role_access
# class TestSuperAdminAccess:
#     """
#     Super Admin — full application access.
#       ✔ All sidebar items visible
#       ✔ Can create all four user types
#       ✔ Can edit / delete any user
#     """
#
#     def test_sa_user_management_visible(self, super_admin_page):
#         super_admin_page.navigate_to_dashboard()
#         super_admin_page.assert_user_management_visible()
#
#     def test_sa_report_registration_visible(self, super_admin_page):
#         super_admin_page.navigate_to_dashboard()
#         super_admin_page.assert_report_registration_visible()
#
#     def test_sa_org_registration_visible(self, super_admin_page):
#         super_admin_page.navigate_to_dashboard()
#         super_admin_page.assert_org_registration_visible()
#
#     def test_sa_can_select_all_user_types(self, super_admin_page):
#         """All four user types are available in the dropdown."""
#         super_admin_page.navigate_to_dashboard()
#         super_admin_page.open_user_management()
#         super_admin_page.new_user_btn.click()
#         for user_type in ["Super Admin", "Signa User", "Organization Admin", "Organization User"]:
#             super_admin_page.assert_user_type_option_present(user_type)
#
#     def test_sa_can_create_all_user_types(self, super_admin_page, super_admin_data):
#         """Super Admin creates one user of each type — all deleted in teardown."""
#         for user in super_admin_data["create_users"]:
#             super_admin_page.navigate_to_dashboard()
#             super_admin_page.open_user_management()
#             super_admin_page.fill_minimal_user_form(
#                 first=user["firstName"],
#                 last=user["lastName"],
#                 username=user["username"],
#                 email=user["email"],
#                 user_type=user["userType"],
#                 role=user["role"],
#                 org=user["organization"],
#             )
#             super_admin_page.submit_and_verify_created(
#                 track_in=super_admin_data,
#                 username=user["username"],
#             )
#
#     def test_sa_can_edit_any_user(self, super_admin_page, super_admin_data):
#         """Edit button visible for all users created in this session."""
#         super_admin_page.navigate_to_dashboard()
#         super_admin_page.open_user_management()
#         for user in super_admin_data["create_users"]:
#             super_admin_page.assert_edit_button_visible_for(user["username"])
#
#     def test_sa_can_delete_any_user(self, super_admin_page, super_admin_data):
#         """Delete button visible for all users created in this session."""
#         super_admin_page.navigate_to_dashboard()
#         super_admin_page.open_user_management()
#         for user in super_admin_data["create_users"]:
#             super_admin_page.assert_delete_button_visible_for(user["username"])
#

# ══════════════════════════════════════════════════════════════════════════════
# TC-SU: Signa User
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.role_access
class TestSignaUserAccess:
    """
    Signa User — full access except Super Admin management.
      ✔ All sidebar items visible
      ✔ Can create Org Admin and Org User
      ✖ Cannot create Super Admin
      ✖ Cannot view / edit / delete Super Admin
    """

    def test_su_user_management_visible(self, signa_user_page):
        signa_user_page.navigate_to_dashboard()
        signa_user_page.assert_user_management_visible()


    def test_su_report_registration_visible(self, signa_user_page):
        signa_user_page.navigate_to_dashboard()
        signa_user_page.assert_report_registration_visible()

    def test_su_org_registration_visible(self, signa_user_page):
        signa_user_page.navigate_to_dashboard()
        signa_user_page.assert_org_registration_visible()
    #
    # def test_su_cannot_select_super_admin_user_type(self, signa_user_page):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.new_user_btn.click()
    #     signa_user_page.assert_user_type_option_absent("Super Admin")
    #
    # def test_su_can_select_allowed_user_types(self, signa_user_page):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.new_user_btn.click()
    #     for user_type in ["Signa User", "Organization Admin", "Organization User"]:
    #         signa_user_page.assert_user_type_option_present(user_type)
    #
    # def test_su_can_create_allowed_user_types(self, signa_user_page, signa_user_data):
    #     """Signa User creates Org Admin and Org User — deleted in teardown."""
    #     for user in signa_user_data["create_users"]:
    #         signa_user_page.navigate_to_dashboard()
    #         signa_user_page.open_user_management()
    #         signa_user_page.fill_minimal_user_form(
    #             first=user["firstName"],
    #             last=user["lastName"],
    #             username=user["username"],
    #             email=user["email"],
    #             user_type=user["userType"],
    #             role=user["role"],
    #             org=user["organization"],
    #         )
    #         signa_user_page.submit_and_verify_created(
    #             track_in=signa_user_data,
    #             username=user["username"],
    #         )
    #
    # def test_su_cannot_view_super_admin_in_table(self, signa_user_page, seeded_users):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.assert_user_not_visible_in_table(seeded_users["super_admin"])
    #
    # def test_su_cannot_edit_super_admin(self, signa_user_page, seeded_users):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.assert_edit_button_hidden_for(seeded_users["super_admin"])
    #
    # def test_su_cannot_delete_super_admin(self, signa_user_page, seeded_users):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.assert_delete_button_hidden_for(seeded_users["super_admin"])
    #
    # def test_su_can_edit_org_user(self, signa_user_page, seeded_users):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.assert_edit_button_visible_for(seeded_users["org_user"])
    #
    # def test_su_can_delete_org_user(self, signa_user_page, seeded_users):
    #     signa_user_page.navigate_to_dashboard()
    #     signa_user_page.open_user_management()
    #     signa_user_page.assert_delete_button_visible_for(seeded_users["org_user"])


# # ══════════════════════════════════════════════════════════════════════════════
# # TC-OA: Organization Admin
# # ══════════════════════════════════════════════════════════════════════════════
#
# @pytest.mark.smoke
# @pytest.mark.role_access
# class TestOrgAdminAccess:
#     """
#     Organization Admin — limited to own org only.
#       ✔ Can create Org Admin and Org User within own org
#       ✔ Can view own org reports
#       ✖ Cannot create Super Admin or Signa User
#       ✖ Cannot see / edit / delete Super Admin or Signa User
#       ✖ No Report Registration or Organization Registration
#     """
#
#     def test_oa_user_management_visible(self, org_admin_page):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.assert_user_management_visible()
#
#     def test_oa_report_registration_hidden(self, org_admin_page):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.assert_report_registration_hidden()
#
#     def test_oa_org_registration_hidden(self, org_admin_page):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.assert_org_registration_hidden()
#
#     def test_oa_cannot_select_restricted_user_types(self, org_admin_page):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.open_user_management()
#         org_admin_page.new_user_btn.click()
#         org_admin_page.assert_user_type_option_absent("Super Admin")
#         org_admin_page.assert_user_type_option_absent("Signa User")
#
#     def test_oa_can_select_allowed_user_types(self, org_admin_page):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.open_user_management()
#         org_admin_page.new_user_btn.click()
#         org_admin_page.assert_user_type_option_present("Organization Admin")
#         org_admin_page.assert_user_type_option_present("Organization User")
#
#     def test_oa_can_create_allowed_user_types(self, org_admin_page, org_admin_data):
#         """Org Admin creates Org Admin and Org User — deleted in teardown."""
#         for user in org_admin_data["create_users"]:
#             org_admin_page.navigate_to_dashboard()
#             org_admin_page.open_user_management()
#             org_admin_page.fill_minimal_user_form(
#                 first=user["firstName"],
#                 last=user["lastName"],
#                 username=user["username"],
#                 email=user["email"],
#                 user_type=user["userType"],
#                 role=user["role"],
#                 org=user["organization"],
#             )
#             org_admin_page.submit_and_verify_created(
#                 track_in=org_admin_data,
#                 username=user["username"],
#             )
#
#     def test_oa_cannot_see_super_admin_in_table(self, org_admin_page, seeded_users):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.open_user_management()
#         org_admin_page.assert_user_not_visible_in_table(seeded_users["super_admin"])
#
#     def test_oa_cannot_see_signa_user_in_table(self, org_admin_page, seeded_users):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.open_user_management()
#         org_admin_page.assert_user_not_visible_in_table(seeded_users["signa_user"])
#
#     def test_oa_cannot_edit_or_delete_signa_user(self, org_admin_page, seeded_users):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.open_user_management()
#         org_admin_page.assert_edit_button_hidden_for(seeded_users["signa_user"])
#         org_admin_page.assert_delete_button_hidden_for(seeded_users["signa_user"])
#
#     def test_oa_can_view_own_org_reports(self, org_admin_page, org_admin_data):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.page.get_by_role("button", name=" Reports", exact=False).click()
#         expect(
#             org_admin_page.page.get_by_text(org_admin_data["expected_report"], exact=False)
#         ).to_be_visible()
#
#     def test_oa_cannot_view_other_org_reports(self, org_admin_page, org_admin_data):
#         org_admin_page.navigate_to_dashboard()
#         org_admin_page.page.get_by_role("button", name=" Reports", exact=False).click()
#         expect(
#             org_admin_page.page.get_by_text(org_admin_data["other_org_report"], exact=False)
#         ).not_to_be_visible()
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # TC-OU: Organization User
# # ══════════════════════════════════════════════════════════════════════════════
#
# @pytest.mark.smoke
# @pytest.mark.role_access
# class TestOrgUserAccess:
#     """
#     Organization User — own account only.
#       ✔ Can see only their own account
#       ✔ Multi-org assignment visible on profile
#       ✖ No user creation
#       ✖ No Report or Organization Registration
#     """
#
#     def test_ou_report_registration_hidden(self, org_user_page):
#         org_user_page.navigate_to_dashboard()
#         org_user_page.assert_report_registration_hidden()
#
#     def test_ou_org_registration_hidden(self, org_user_page):
#         org_user_page.navigate_to_dashboard()
#         org_user_page.assert_org_registration_hidden()
#
#     def test_ou_cannot_create_any_user(self, org_user_page):
#         org_user_page.navigate_to_dashboard()
#         org_user_page.open_user_management()
#         expect(org_user_page.new_user_btn).not_to_be_visible()
#
#     def test_ou_can_only_see_own_account(self, org_user_page, org_user_data, seeded_users):
#         own_username = org_user_data["credentials"]["username"]
#         org_user_page.navigate_to_dashboard()
#         org_user_page.open_user_management()
#         org_user_page.assert_user_visible_in_table(own_username)
#         for _role, username in seeded_users["all_types"].items():
#             if username != own_username:
#                 org_user_page.assert_user_not_visible_in_table(username)
#
#     def test_ou_cannot_edit_or_delete_any_user(self, org_user_page, seeded_users):
#         org_user_page.navigate_to_dashboard()
#         org_user_page.open_user_management()
#         for _role, username in seeded_users["all_types"].items():
#             org_user_page.assert_edit_button_hidden_for(username)
#             org_user_page.assert_delete_button_hidden_for(username)
#
#     def test_ou_multi_org_assignment_visible(self, org_user_page, org_user_data):
#         own_username = org_user_data["credentials"]["username"]
#         org_user_page.navigate_to_dashboard()
#         org_user_page.open_user_management()
#         org_user_page.search_user(own_username)
#         org_user_page.page.get_by_role("button", name="Edit").first.click()
#         for org in org_user_data["assigned_organizations"]:
#             expect(
#                 org_user_page.page.locator(".MuiAutocomplete-tag", has_text=org)
#             ).to_be_visible()