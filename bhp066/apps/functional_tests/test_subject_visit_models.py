import time
from selenium import webdriver

from .base_selinium_test import BaseSeleniumTest
from .pages import SubjectDasbhoardPage, ResidencyMobilityPage


class SubjectVisitModelsTest(BaseSeleniumTest):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def navigate_subject_dashboard(self):
        self.login()
        sb_dash = SubjectDasbhoardPage(self.browser)
        self.browser.get(sb_dash.subject_dashboard_url)
        sb_dash.click_show_forms_link()

    def test_residency_and_mobility_link(self):
        self.navigate_subject_dashboard()
        self.subject_dash = SubjectDasbhoardPage(self.browser)
        if self.subject_dash.click_residency_mobility_link():
            self.assertIn('/admin/bcpp_subject/residencymobility/add', self.browser.current_url)

    def test_fill_residency_and_mobility(self):
        self.test_residency_and_mobility_link()
        res = ResidencyMobilityPage(self.browser)
        res.fill_residency_mobility(res.select_length_month_6, res.select_permanent_resident_yes,
                                    res.select_intend_residency_yes, res.select_nights_away_wk2, res.select_cattle_postlands_farm)
