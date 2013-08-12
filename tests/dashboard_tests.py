from django.test import TestCase
from bhp_section.classes import site_sections
from bhp_search.classes import site_search
from bcpp_dashboard.classes import HouseholdDashboard, SubjectDashboard


class DashboardTests(TestCase):

    def test_household_dashboard(self):
        site_sections.autodiscover()
        site_search.autodiscover(site_sections.get_section_list())
        dashboard = HouseholdDashboard()

    def test_subject_dashboard(self):
        site_sections.autodiscover()
        site_search.autodiscover(site_sections.get_section_list())
        dashboard = SubjectDashboard()
