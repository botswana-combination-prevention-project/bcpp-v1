from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectVisitPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    report_today = (By.XPATH, "(//form[@id='subjectvisit_form']//descendant::a[text()='Today'])[1]")
    report_now = (By.XPATH, " (//form[@id='subjectvisit_form']//descendant::a[text()='Now'])[1]")

    def click_report_today(self):
        self.browser.find_element(*SubjectVisitPage.report_today).click()

    def click_report_now(self):
        self.browser.find_element(*SubjectVisitPage.report_now).click()

    def set_consent_date(self, report_date):
        visitdate_element = self.browser.find_element(*SubjectVisitPage.report_date)
        visitdate_element.send_keys(report_date)

    def set_consent_time(self, report_time):
        visittime_element = self.browser.find_element(*SubjectVisitPage.report_time)
        visittime_element.send_keys(report_time)

    def fill_subject_visit(self, report_date=None, report_time=None):
        if report_date:
            self.set_consent_date(report_date)
        else:
            self.click_report_today()
        if report_time:
            self.set_consent_time(report_time)
        else:
            self.click_report_now()
        self.click_save_button()
