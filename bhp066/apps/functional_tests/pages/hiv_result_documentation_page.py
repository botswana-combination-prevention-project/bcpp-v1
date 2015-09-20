from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HivResultDocumentationPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_0')
    result_date = (By.ID, 'id_result_date')
    result_doc_type = (By.ID, 'id_result_doc_type')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*HivResultDocumentationPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*HivResultDocumentationPage.report_time)
        time_element.send_keys(report_time)

    def set_has_tested(self, result_date):
        result_date_element = self.browser.find_element(*HivResultDocumentationPage.result_date)
        result_date_element.send_keys(result_date)

    def set_other_record(self, result_doc_type):
        result_doc_type_element = self.browser.find_element(*HivResultDocumentationPage.result_doc_type)
        result_doc_type_element.send_keys(result_doc_type)

    def fill_hiv_result_documentation(self, report_date, report_time, result_date, result_doc_type):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.result_date(result_date)
        self.result_doc_type(result_doc_type)
        self.save_button()
