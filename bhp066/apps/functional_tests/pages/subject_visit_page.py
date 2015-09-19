from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectVisitPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')

    def set_consent_date(self, report_date):
        visitdate_element = self.browser.find_element(*SubjectVisitPage.report_date)
        visitdate_element.send_keys(report_date)

    def set_consent_time(self, report_time):
        visittime_element = self.browser.find_element(*SubjectVisitPage.report_time)
        visittime_element.send_keys(report_time)

    def fill_subject_visit(self, report_date=None, report_time=None):
        self.set_consent_date(report_date)
        self.set_consent_time(report_time)
