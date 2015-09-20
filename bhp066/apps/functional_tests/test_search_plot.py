import time
 
from .base_selinium_test import BaseSeleniumTest
 
from .pages import (
    SearchPage, PlotResultPage, PlotLogEntryPage, PlotPage, PlotDashboardPage,
    HouseholdDashboardPage, HouseholdLogEntryPage, HouseholdMemberPage,
    CheckEligibilityPage, SubjectDasbhoardPage, SubjectConsentPage
)
 
 
class TestSearchPlotSeleniumTest(BaseSeleniumTest):
 
    def setUp(self):
        self.search_page = SearchPage
        self.plot_result_page = PlotResultPage
        self.plot_log_entry_page = PlotLogEntryPage
        self.plot_page = PlotPage
        self.plot_dashboard_page = PlotDashboardPage
        self.household_dashboard_pg = HouseholdDashboardPage
        self.household_log_entry = HouseholdLogEntryPage
        self.household_member_pg = HouseholdMemberPage
        self.check_eligibility = CheckEligibilityPage
        self.subject_dashboard_pg = SubjectDasbhoardPage
        self.subject_consent_pg = SubjectConsentPage
 
    def test_search_plot(self):
        self.login()
        time.sleep(1)
        self.plot_result_page.click_plotlink()
        time.sleep(1)
        self.search_page.search('400007-03')
        time.sleep(2)
        self.plot_result_page.click_addnewentry()
        time.sleep(1)
        self.plot_log_entry_page.fill_plot_log_entry()
        time.sleep(1)
        self.plot_result_page.get_plot('400007-03')
        time.sleep(1)
        self.plot_page.fill_plot_change('residential_habitable', 25, 25, 90, 25, 1)
        time.sleep(1)
        self.search_page.search('400007-03')
        time.sleep(1)
        self.plot_result_page.click_household()
        time.sleep(1)
        self.plot_dashboard_page.click_composition()
        time.sleep(1)
        self.household_dashboard_pg.click_add_househouldentry()
        time.sleep(1)
        self.household_log_entry.fill_household_entry()
        time.sleep(1)
        self.household_log_entry.click_add_householdmember()
        self.household_member_pg.fill_householdmember(
            "Mochine", "MW", "M", 25, "N/A", "Yes", "Head", "Yes")
        time.sleep(1)
        self.household_dashboard_pg.click_check_eligibility()
        time.sleep(1)
        self.check_eligibility.fill_check_eligibilty("MW", "M", "Yes", "Yes", "N/A", "Continue", "Yes")
        time.sleep(1)
        self.subject_dashboard_pg.click_new_subject_consent()
        time.sleep(1)
        self.subject_consent_pg.fill_consent("Mochine", "Wannota", "WM", self.subject_consent_pg.select_en_language, self.subject_consent_pg.is_literate, "2015-09-17", "16:30:00",
                     "M", "1990-09-17", "No", "Yes", "334213215", "334213215", "Yes",
                     "Yes", "Yes", "Yes", "Yes", "Yes")
        time.sleep(1)
