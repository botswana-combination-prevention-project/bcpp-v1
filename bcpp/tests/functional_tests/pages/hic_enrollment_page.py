from selenium.webdriver.common.by import By
from .base_page import BasePage


class HicEnrollmentPage(BasePage):
    consent_version = (By.ID, 'id_consent_version')
    report_date = (By.ID, 'report_datetime_0')
    report_time = (By.ID, 'report_datetime_1')
    today = (By.XPATH, ".//*[@id='hicenrollment_form']/div/fieldset/div[3]/div/p[1]/span[1]/a[1]")
    now = (By.XPATH, ".//*[@id='hicenrollment_form']/div/fieldset/div[3]/div/p[1]/span[2]/a[1]")
    hic_permission = (By.ID, 'id_hic_permission')
    save_button = (By.NAME, "_save")

    def set_report_date(self, date):
        dateElement = self.browser.find_element(*HicEnrollmentPage.report_date)
        dateElement.send_keys(date)

    def set_report_time(self, time):
        dateElement = self.browser.find_element(*HicEnrollmentPage.report_time)
        dateElement.send_keys(time)

    def set_consent_version(self, consent_version):
        consentElement = self.browser.find_element(*HicEnrollmentPage.consent_version)
        consentElement.send_keys(consent_version)

    def click_today(self):
        self.browser.find_element(*HicEnrollmentPage.today).click()

    def click_now(self):
        self.browser.find_element(*HicEnrollmentPage.now).click()

    def fill_hic_enrollment(self, date=None, time=None, consent_version):
        if not date:
            self.click_today()
        else:
            self.set_report_date(date)
        if not time:
            self.click_now()
        else:
            self.set_report_time(time)
        self.set_consent_version(consent_version)
        self.click_save_button()
