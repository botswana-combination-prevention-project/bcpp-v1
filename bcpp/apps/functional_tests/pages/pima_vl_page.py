from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class PimaVlPage(BaseModelAdminPage):
    consent_version = (By.ID, 'id_consent_version')
    report_date = (By.ID, 'report_datetime_0')
    report_time = (By.ID, 'report_datetime_1')
    today = (By.XPATH, "//form[@id='plotlogentry_form']/descendant::a[text()='Today']")
    now = (By.XPATH, "//form[@id='plotlogentry_form']/descendant::a[text()='Now']")
    poc_vl_today = (By.ID, 'id_poc_vl_today_0')
    quantifier_greater_than = (By.XPATH, ".//*[@id='id_vl_value_quatifier']/option[2]")
    ease_of_use = (By.XPATH, ".//*[@id='id_easy_of_use']/li[1]/label")
    save_button = (By.NAME, "_save")

    def set_report_date(self, date):
        dateElement = self.browser.find_element(*PimaVlPage.report_date)
        dateElement.send_keys(date)

    def set_report_time(self, time):
        dateElement = self.browser.find_element(*PimaVlPage.report_time)
        dateElement.send_keys(time)

    def set_pov_vl_today(self):
        self.browser.find_element(*PimaVlPage.poc_vl_today).click()

    def set_quantifier_greater_than(self):
        self.browser.find_element(*PimaVlPage.quantifier_greater_than).click()

    def set_ease_of_use(self):
        self.browser.find_element(*PimaVlPage.ease_of_use).click()

    def fill_pima_vl_page(self, date=None, time=None):
        if not date:
            self.click_today()
        else:
            self.set_report_date(date)
        if not time:
            self.click_now()
        else:
            self.set_report_time(time)
        self.set_pov_vl_today()
        self.set_quantifier_greater_than()
        self.set_ease_of_use()
