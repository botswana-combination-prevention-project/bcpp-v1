from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HouseholdLogEntryPage(BaseModelAdminPage):

    report_date = (By.ID, 'id_report_datetime')
    today = (By.XPATH, "//form[@id='householdlogentry_form']/descendant::a[text()='Today']")
    household_status = (By.ID, 'id_household_status')
    eligible_present = (By.ID, 'id_household_status_0')
    eligible_absent = (By.ID, 'id_household_status_1')
    no_household_info = (By.ID, 'id_household_statu_2')
    refused_enum = (By.ID, 'id_household_status_3')

    def set_report_date(self, report_date):
        dateElement = self.browser.find_element(*HouseholdLogEntryPage.report_date).click()
        dateElement.send_keys(report_date)

    def select_today(self):
        self.browser.find_element(*HouseholdLogEntryPage.today).click()

    def fill_household_entry(self, report_date=None):
        if not report_date:
            self.set_report_date(report_date)
        else:
            self.select_today()
        self.click_save()
