from selenium import webdriver
from .base_selinium_test import BaseSeleniumTest

from .pages import SubjectDasbhoardPage, SubjectLocatorPage


class TestSubjectVisits(BaseSeleniumTest):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def open_subject_dashboard(self):
        self.login()
        sb_dash = SubjectDasbhoardPage(self.browser)
        self.browser.get(sb_dash.subject_dashboard_url)
        sb_dash.click_show_forms_link()

    def test_subject_locator_link(self):
        self.open_subject_dashboard()
        self.subject_dash = SubjectDasbhoardPage(self.browser)
        if self.subject_dash.click_subject_locator_link():
            self.assertIn('/admin/bcpp_subject/subjectlocator/add', self.browser.current_url)

    def test_fill_subject_locator_page(self):
        self.test_subject_locator_link()
        locator = SubjectLocatorPage(self.browser)
        locator.fill_subject_locator(
            locator.select_home_visit_permission_yes, locator.select_may_follow_up_yes,
            locator.select_may_sms_follow_up_yes, locator.select_may_call_work_yes,
            locator.select_may_contact_someone_yes, locator.select_has_alt_contact_yes
        )
