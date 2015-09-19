from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HivUntestedPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    have_pills = (By.ID, 'id_have_pills')
    why_no_hiv_test = (By.ID, 'id_why_no_hiv_test')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*HivUntestedPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*HivUntestedPage.report_time)
        time_element.send_keys(report_time)

    def set_have_pills(self, have_pills):
        have_pills_element = self.browser.find_element(*HivUntestedPage.have_pills)
        have_pills_element.send_keys(have_pills)

    def set_why_no_hiv_test(self, why_no_hiv_test):
        why_no_hiv_test_element = self.browser.find_element(*HivUntestedPage.why_no_hiv_test)
        why_no_hiv_test_element.send_keys(why_no_hiv_test)

    def fill_hiv_testing_history(self, report_date, report_time, have_pills, why_no_hiv_test):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.set_have_pills(have_pills)
        self.set_why_no_hiv_test(why_no_hiv_test)
        self.save_button()
