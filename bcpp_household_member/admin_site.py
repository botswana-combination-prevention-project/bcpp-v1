from django.contrib.admin import AdminSite


class BcppHouseholdMemberAdminSite(AdminSite):
    site_title = 'BCPP Householdmember'
    site_header = 'BCPP Householdmember'
    index_title = 'BCPP Householdmember'
    site_url = '/'
bcpp_household_member_admin = BcppHouseholdMemberAdminSite(name='bcpp_household_member_admin')
