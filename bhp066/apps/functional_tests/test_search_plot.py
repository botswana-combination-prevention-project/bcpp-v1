import time
from selenium import webdriver
from .base_selinium_test import BaseSeleniumTest

from .pages import (
    SearchPage, PlotResultPage, PlotLogEntryPage, PlotPage, PlotDashboardPage,
    HouseholdDashboardPage, HouseholdLogEntryPage, HouseholdMemberPage,
    CheckEligibilityPage, SubjectDasbhoardPage, SubjectConsentPage, HomePage
)


class TestSearchPlotSeleniumTest(BaseSeleniumTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.search_page = SearchPage
        self.plot_result_page = PlotResultPage
        self.plot_dashboard_page = PlotDashboardPage
        self.household_dashboard_pg = HouseholdDashboardPage
        self.household_log_entry = HouseholdLogEntryPage
        self.household_member_pg = HouseholdMemberPage
        self.check_eligibility = CheckEligibilityPage
        self.subject_dashboard_pg = SubjectDasbhoardPage
        self.subject_consent_pg = SubjectConsentPage

    def test_home(self):
        self.home_pg = HomePage(self.browser)
        self.login()
        time.sleep(1)
        self.home_pg.click_plot()
        time.sleep(1)

    def test_search_plot(self):
        self.home_pg = HomePage(self.browser)
        self.login()
        time.sleep(1)
        self.home_pg.click_plot()
        time.sleep(1)
        self.search_page = SearchPage(self.browser)
        self.search_page.search('390112-08')

    def test_plot_log_entry_link(self):
        self.test_search_plot()
        self.plot_result_page = PlotResultPage(self.browser)
        self.plot_result_page.click_addnewentry()

    def test_add_plot_log_entry(self):
        self.test_plot_log_entry_link()
        self.plot_log_entry_pg = PlotLogEntryPage(self.browser)
        self.plot_log_entry_pg.fill_plot_log_entry(plot_status=self.plot_log_entry_pg.select_accessible)

    def test_plot_link(self):
        self.test_search_plot()
        self.plot_result_page = PlotResultPage(self.browser)
        self.plot_result_page.click_plotlink()

    def test_confirm_plot(self):
        self.test_plot_link()
        plot_page = PlotPage(self.browser)
        plot_page.fill_plot_change(plot_page.select_res_habit, 25, 25, 90, 25, 1, plot_page.select_weekdays, plot_page.select_morning)

    def test_household_link(self):
        self.test_search_plot()
        self.plot_result_page = PlotResultPage(self.browser)
        self.plot_result_page.click_household()

    def test_households_composition_link(self):
        self.test_household_link()
        self.plot_result_page = PlotDashboardPage(self.browser)
        self.plot_result_page.click_composition()

    def test_add_household_log_link(self):
        self.test_households_composition_link()
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.household_dashboard_page.click_add_househouldentry()

    def test_add_household_log(self):
        self.test_add_household_log_link()
        self.household_log_entry_page = HouseholdLogEntryPage(self.browser)
        self.household_log_entry_page.fill_household_entry(self.household_log_entry_page.select_eligible_present)


#     def test_search_plot1(self):
#         self.login()
#         time.sleep(1)
#         self.search_page.search('390112-08')
#         self.plot_result_page.click_plotlink()
#         time.sleep(1)
#         self.search_page.search('400007-03')
#         time.sleep(2)
#         self.plot_result_page.click_addnewentry()
#         time.sleep(1)
#         self.plot_log_entry_page.fill_plot_log_entry()
#         time.sleep(1)
#         self.plot_result_page.get_plot('400007-03')
#         time.sleep(1)
#         self.plot_page.fill_plot_change('residential_habitable', 25, 25, 90, 25, 1)
#         time.sleep(1)
#         self.search_page.search('400007-03')
#         time.sleep(1)
#         self.plot_result_page.click_household()
#         time.sleep(1)
#         self.plot_dashboard_page.click_composition()
#         time.sleep(1)
#         self.household_dashboard_pg.click_add_househouldentry()
#         time.sleep(1)
#         self.household_log_entry.fill_household_entry()
#         time.sleep(1)
#         self.household_log_entry.click_add_householdmember()
#         self.household_member_pg.fill_householdmember(
#             "Mochine", "MW", "M", 25, "N/A", "Yes", "Head", "Yes")
#         time.sleep(1)
#         self.household_dashboard_pg.click_check_eligibility()
#         time.sleep(1)
#         self.check_eligibility.fill_check_eligibilty("MW", "M", "Yes", "Yes", "N/A", "Continue", "Yes")
#         time.sleep(1)
#         self.subject_dashboard_pg.click_new_subject_consent()
#         time.sleep(1)
#         self.subject_consent_pg.fill_consent("Mochine", "Wannota", "WM", self.subject_consent_pg.select_en_language, self.subject_consent_pg.is_literate, "2015-09-17", "16:30:00",
#                      "M", "1990-09-17", "No", "Yes", "334213215", "334213215", "Yes",
#                      "Yes", "Yes", "Yes", "Yes", "Yes")
#         time.sleep(1)
