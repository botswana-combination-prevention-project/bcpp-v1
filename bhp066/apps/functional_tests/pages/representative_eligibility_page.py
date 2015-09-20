from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class RepresentativeEligibilityPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_0')
    aged_over_18 = (By.ID, 'id_aged_over_18')
    aged_over_18_yes = (By.ID, 'id_aged_over_18_0')
    aged_over_18_no = (By.ID, 'id_aged_over_18_1')
    household_residency = (By.ID, 'id_household_residency')
    household_residency_yes = (By.ID, 'id_household_residency_0')
    household_residency_no = (By.ID, 'id_household_residency_1')
    verbal_script = (By.ID, 'id_verbal_script')
    verbal_script_yes = (By.ID, 'id_verbal_script_0')
    verbal_script_no = (By.ID, 'id_verbal_script_1')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*RepresentativeEligibilityPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*RepresentativeEligibilityPage.report_time)
        time_element.send_keys(report_time)

    def set_aged_over_18(self, aged_over_18):
        aged_over_18.click()

    @property
    def select_aged_over_18_yes(self):
        return self.browser.find_element(*RepresentativeEligibilityPage.aged_over_18_yes)

    @property
    def select_aged_over_18_no(self):
        return self.browser.find_element(*RepresentativeEligibilityPage.aged_over_18_no)

    def set_household_residency(self, household_residency):
        household_residency.click()

    @property
    def select_household_residency_yes(self):
        return self.browser.find_element(*RepresentativeEligibilityPage.household_residency_yes)

    @property
    def select_household_residency_no(self):
        return self.browser.find_element(*RepresentativeEligibilityPage.household_residency_no)

    def set_verbal_script(self, verbal_script):
        verbal_script.click()

    @property
    def select_verbal_script_yes(self):
        return self.browser.find_element(*RepresentativeEligibilityPage.verbal_script_yes)

    @property
    def select_verbal_script_no(self):
        return self.browser.find_element(*RepresentativeEligibilityPage.verbal_script_no)

    def fill_representative_eligibility(self, report_date, report_time, aged_over_18, household_residency,
                                        verbal_script):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.set_aged_over_18(aged_over_18)
        self.household_residency(household_residency)
        self.verbal_script(verbal_script)
        self.click_save_button()