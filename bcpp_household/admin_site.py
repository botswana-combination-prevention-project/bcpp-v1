from django.contrib.admin import AdminSite


class BcppHouseholdAdminSite(AdminSite):
    site_title = 'BCPP Household'
    site_header = 'BCPP Household'
    index_title = 'BCPP Household'
    site_url = '/'
bcpp_household_admin = BcppHouseholdAdminSite(name='bcpp_household_admin')
