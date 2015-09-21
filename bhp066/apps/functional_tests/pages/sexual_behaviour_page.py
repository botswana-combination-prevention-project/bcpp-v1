from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SexualBehaviourPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    ever_sex = (By.ID, 'id_ever_sex')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*SexualBehaviourPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*SexualBehaviourPage.report_time)
        time_element.send_keys(report_time)

    def set_have_pills(self, ever_sex):
        ever_sex_element = self.browser.find_element(*SexualBehaviourPage.ever_sex)
        ever_sex_element.send_keys(ever_sex)

    def fill_sexual_behaviour(self, report_date, report_time, ever_sex):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.set_ever_sex(ever_sex)
        self.save_button()
