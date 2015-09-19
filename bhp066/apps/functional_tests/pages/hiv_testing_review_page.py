from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HivTestingReviewPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    has_tested = (By.ID, 'id_has_tested')
    other_record = (By.ID, 'id_other_record')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*HivTestingReviewPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*HivTestingReviewPage.report_time)
        time_element.send_keys(report_time)

    def set_has_tested(self, has_tested):
        has_tested_element = self.browser.find_element(*HivTestingReviewPage.has_tested)
        has_tested_element.send_keys(has_tested)

    def set_other_record(self, other_record):
        other_record_element = self.browser.find_element(*HivTestingReviewPage.other_record)
        other_record_element.send_keys(other_record)

    def fill_hiv_testing_review(self, report_date, report_time, has_tested, other_record):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.set_has_tested(has_tested)
        self.set_other_record(other_record)
        self.save_button()
