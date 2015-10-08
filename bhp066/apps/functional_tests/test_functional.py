from selenium import webdriver

from ..bcpp_household.models import Plot, PlotLog

from .base_selinium_test import BaseSeleniumTest
from .pages import (
    SearchPage, PlotResultPage, PlotLogEntryPage, PlotPage, PlotDashboardPage,
    HouseholdDashboardPage, HouseholdLogEntryPage, HouseholdMemberPage,
    SubjectDasbhoardPage, HomePage, CheckEligibilityPage, SubjectConsentPage, SubjectVisitPage,
    RepresentativeEligibilityPage, HouseholdHeadEligibilityPage, HouseholdHeadInfoPage
)
import time


class FunctionalSeleniumTest(BaseSeleniumTest):

    def setUp(self):
        super(FunctionalSeleniumTest, self).setUp()
        self.search_page = SearchPage
        self.plot_result_page = PlotResultPage
        self.plot_dashboard_page = PlotDashboardPage
        self.household_dashboard_pg = HouseholdDashboardPage
        self.household_log_entry = HouseholdLogEntryPage
        self.household_member_pg = HouseholdMemberPage
        self.check_eligibility = CheckEligibilityPage
        self.subject_dashboard_pg = SubjectDasbhoardPage
        self.subject_consent_pg = SubjectConsentPage
        self.plot = Plot.objects.all()[0]
        self.login()

    def test_home(self):
        self.home_pg = HomePage(self.browser)
        self.assertIn('/bcpp/section/', self.browser.current_url)

    def test_search_plot(self):
        HomePage(self.browser).click_plot()
        self.search_page = SearchPage(self.browser)
        self.search_page.search(self.plot.plot_identifier)
        self.assertTrue(self.search_page.is_search_table_visible)

    def test_plot_log_entry_link(self):
        self.browser.get(
            self.live_server_url + '/bcpp_household/bcpp/create_plot_log/?plot={}'.format(self.plot.id))
        self.plot_result_page = PlotResultPage(self.browser)
        self.plot_result_page.click_addnewentry()
        self.assertTrue('/plotlogentry/', self.browser.current_url)

    def test_add_plot_log_entry(self):
        self.browser.get(
            self.live_server_url + '/admin/bcpp_household/plotlogentry/add/?plot_log={}&next=/bcpp/section/plot/'.format(self.plot.id)
        )
        self.plot_log_entry_pg = PlotLogEntryPage(self.browser)
        self.plot_log_entry_pg.fill_plot_log_entry(self.plot_log_entry_pg.select_accessible)
#         self.search_plot()
#         self.assertIn('accessible', PlotResultPage(self.browser).plot_log_entry_link_elem().text)

    def plot_link(self):
        self.plot_result_page = PlotResultPage(self.browser)
        self.plot_result_page.click_plotlink()
        self.assertIn('http://localhost:8000/admin/bcpp_household/plot/', self.browser.current_url)

    def confirm_plot(self):
        self.add_plot_log_entry()
        self.plot_link()
        plot_page = PlotPage(self.browser)
        self.plot_result = PlotResultPage(self.browser)
        plot_page.fill_plot_change(plot_page.select_res_habit, 25, 25, 90, 25, 1, plot_page.select_weekdays, plot_page.select_morning)
        self.search_plot()
        self.assertEqual(self.plot_result.action_status_elem().text, 'confirmed')

    def household_link(self):
        self.plot_result_page = PlotResultPage(self.browser)
        self.plot_result_page.click_household()
        self.assertIn("http://localhost:8000/bcpp/section/household/word/", self.browser.current_url)

    def households_composition_link(self):
        self.plot_result_page = PlotDashboardPage(self.browser)
        self.plot_result_page.click_composition()
        self.assertIn("http://localhost:8000/bcpp/dashboard/household/household_structure", self.browser.current_url)

    def add_household_log_link(self):
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.household_dashboard_page.click_add_househouldentry()
        self.assertIn("http://localhost:8000/admin/bcpp_household/householdlogentry/add/", self.browser.current_url)

    def add_household_log(self):
        self.add_household_log_link()
        self.household_log_entry_page = HouseholdLogEntryPage(self.browser)
        self.household_log_entry_page.fill_household_entry(self.household_log_entry_page.select_eligible_present)
        self.dash = HouseholdDashboardPage(self.browser)
        self.assertTrue(self.dash.is_fill_representative_link_visible)

    def representative_checklist_link(self):
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        if self.household_dashboard_page.click_fill_representative:
            self.assertIn('http://localhost:8000/admin/bcpp_household/representativeeligibility/add/', self.browser.current_url)

    def fill_representative_checklist(self):
        self.representative_checklist_link()
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.r_check_pg = RepresentativeEligibilityPage(self.browser)
        self.r_check_pg.fill_representative_eligibility(
            self.r_check_pg.select_aged_over_18_yes, self.r_check_pg.select_household_residency_yes, self.r_check_pg.select_verbal_script_yes
        )
        self.assertFalse(
            HouseholdDashboardPage(self.browser).is_fill_representative_link_visible
        )

    def add_another_household_member_link(self):
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.household_dashboard_page.click_add_householdmember()
        self.assertIn('http://localhost:8000/admin/bcpp_household_member/householdmember/add/', self.browser.current_url)

    def add_another_household_member(self):
        self.add_another_household_member_link()
        hhm = HouseholdMemberPage(self.browser)
        hhm.fill_householdmember(
            'SETS', 'SA', hhm.select_male, 25, hhm.select_present_today_yes, hhm.select_can_participate,
            hhm.select_study_resident_yes, hhm.select_head
        )

    def hod_eligibility_checklist_link(self):
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.household_dashboard_page.click_hod_eligibility_checklist_link
        self.assertIn('http://localhost:8000/admin/bcpp_household_member/householdheadeligibility/add/', self.browser.current_url)

    def add_hod_eligibility_checklist(self):
        self.hod_eligibility_checklist_link()
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        if not self.household_dashboard_page.click_hod_eligibility_checklist_link:
            hod = HouseholdHeadEligibilityPage(self.browser)
            hod.fill_representative_eligibility(hod.select_aged_over_18_yes, hod.select_household_residency_yes, hod.select_verbal_script_yes)
        self.assertTrue(self.household_dashboard_page.click_household_info_link_visible)

    def household_info_link(self):
        self.hod_eligibility_checklist_link()
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.assertTrue(self.household_dashboard_page.click_household_info_link)

    def add_household_head_info(self):
        self.household_info_link()
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        hhi = HouseholdHeadInfoPage(self.browser)
        hhi.fill_household_info(
            hhi.select_flooring_tile, hhi.select_water_tap, hhi.select_toilet_flush, hhi.select_sm_meals_often
        )
        self.assertIn("http://localhost:8000/bcpp/dashboard/household/household_structure", self.browser.current_url)

    def check_eligibility_link(self):
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.household_dashboard_page.click_check_eligibility_link()
        self.assertIn("http://localhost:8000/admin/bcpp_household_member/enrollmentchecklist/add/", self.browser.current_url)

    def add_check_eligibility(self):
        self.check_eligibility_link()
        el = CheckEligibilityPage(self.browser)
        el.fill_check_eligibilty(
            '1990-09-20', 'SA', el.select_male, el.select_identity_yes, el.select_citizen_yes, el.select_study_participation_yes,
            el.select_legal_marriage_na, el.select_part_time_resident_yes, el.select_household_residencyt_yes, el.select_literacy_yes,
            el.select_guardian_na, el.select_confirm_participation_no, el.select_marriage_certificate_na
        )
        self.assertIn("http://localhost:8000/bcpp/dashboard/household/household_structure", self.browser.current_url)

    def dashboard_link(self):
        self.household_dashboard_page = HouseholdDashboardPage(self.browser)
        self.household_dashboard_page.click_subject_consent()
        self.assertIn("http://localhost:8000/bcpp/dashboard/subject/household_member/", self.browser.current_url)

    def consent_link(self):
        sb_dash = SubjectDasbhoardPage(self.browser)
        sb_dash.click_new_subject_consent()
        self.assertIn("http://localhost:8000/admin/bcpp_subject/subjectconsent/", self.browser.current_url)

    def add_consent(self):
        self.consent_link()
        con = SubjectConsentPage(self.browser)
        con.fill_consent('SETS', 'ANDERSON', 'AD', con.select_language_en, con.select_is_literate_yes, con.select_male, "1990-09-20",
                         con.select_dob_estimated_no, con.select_citizen_yes, "317918511", con.select_identity_omang, "317918511", con.select_store_samples_yes,
                         con.select_consent_reviewed_yes, con.select_study_questions_yes, con.select_assessment_score_yes,
                         con.select_consent_signature_yes, con.select_consent_copy_yes, legal_marriage=con.select_legal_marriage_na,
                         marriage_certificate=con.select_marriage_certificate_na)
        self.assertIn("http://localhost:8000/bcpp/dashboard/subject/household_member/", self.browser.current_url)

    def subject_visit_link(self):
        sb_dash = SubjectDasbhoardPage(self.browser)
        sb_dash.click_new_visit_link()
        self.assertIn("http://localhost:8000/admin/bcpp_subject/subjectvisit/add/", self.browser.current_url)

    def add_subject_visit(self):
        self.subject_visit_link()
        sb_dash = SubjectDasbhoardPage(self.browser)
        sb_dash.click_new_visit_link()
        visit = SubjectVisitPage(self.browser)
        visit.fill_subject_visit()
        self.assertTrue(sb_dash.is_show_forms_link_visible())

    def test_consent(self):
        self.confirm_plot()
        time.sleep(1)
        self.household_link()
        time.sleep(1)
        self.households_composition_link()
        time.sleep(1)
        self.add_household_log()
        time.sleep(1)
        self.fill_representative_checklist()
        time.sleep(1)
        self.add_another_household_member()
        time.sleep(1)
        self.add_hod_eligibility_checklist()
        time.sleep(1)
        self.add_check_eligibility()
        time.sleep(1)
        self.dashboard_link()
        time.sleep(1)
        self.add_consent()
        time.sleep(1)
        self.add_subject_visit()
        time.sleep(1)
