from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HivTestingHistoryPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    report_today = (By.XPATH, "(//form[@id='hivtestinghistory_form']//descendant::a[text()='Today'])[1]")
    report_now = (By.XPATH, " (//form[@id='hivtestinghistory_form']//descendant::a[text()='Now'])[1]")
    has_tested = (By.ID, 'id_has_tested')
    other_record = (By.ID, 'id_other_record')

    def click_report_today(self):
        self.browser.find_element(*HivTestingHistoryPage.report_today).click()

    def click_report_now(self):
        self.browser.find_element(*HivTestingHistoryPage.report_now).click()

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*HivTestingHistoryPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*HivTestingHistoryPage.report_time)
        time_element.send_keys(report_time)

    def select_has_tested_yes(self):
        pass

    def select_has_tested_no(self):
        pass

    def select_when_last_tested_in_1_to_5(self):
        pass

    def select_record_available_yes(self):
        pass

    def select_record_available_no(self):
        pass

    def select_hiv_result_neg(self):
        pass

    def select_hiv_result_pos(self):
        pass

    def select_doc_yes(self):
        pass

    def select_doc_no(self):
        pass

    def set_has_tested(self, has_tested):
        has_tested_element = self.browser.find_element(*HivTestingHistoryPage.has_tested)
        has_tested_element.send_keys(has_tested)

    def set_other_record(self, other_record):
        other_record_element = self.browser.find_element(*HivTestingHistoryPage.other_record)
        other_record_element.send_keys(other_record)

    def fill_hiv_testing_history(self, has_tested, other_record, report_date=None, report_time=None):
        if report_date:
            self.set_report_date(report_date)
        else:
            self.click_report_today()
        if report_time:
            self.set_report_time(report_time)
        else:
            self.click_report_now()
        self.set_has_tested(has_tested)
        self.set_other_record(other_record)
        self.save_button()
