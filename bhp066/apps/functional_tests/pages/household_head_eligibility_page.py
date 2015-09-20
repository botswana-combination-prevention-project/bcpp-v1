from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HouseholdHeadEligibilityPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_0')
    report_today = (By.XPATH, "(//form[@id='householdheadeligibility_form']//descendant::a[text()='Today'])[1]")
    report_now = (By.XPATH, " (//form[@id='householdheadeligibility_form']//descendant::a[text()='Now'])[1]")
    household_member = (By.XPATH, "//select[@id='id_household_member']/option[2]")
    aged_over_18 = (By.ID, 'id_aged_over_18')
    aged_over_18_yes = (By.ID, 'id_aged_over_18_0')
    aged_over_18_no = (By.ID, 'id_aged_over_18_1')
    household_residency = (By.ID, 'id_household_residency')
    household_residency_yes = (By.ID, 'id_household_residency_0')
    household_residency_no = (By.ID, 'id_household_residency_1')
    verbal_script = (By.ID, 'id_verbal_script')
    verbal_script_yes = (By.ID, 'id_verbal_script_0')
    verbal_script_no = (By.ID, 'id_verbal_script_1')

    def click_report_today(self):
        self.browser.find_element(*HouseholdHeadEligibilityPage.report_today).click()

    def click_report_now(self):
        self.browser.find_element(*HouseholdHeadEligibilityPage.report_now).click()

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*HouseholdHeadEligibilityPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*HouseholdHeadEligibilityPage.report_time)
        time_element.send_keys(report_time)

    def set_aged_over_18(self, aged_over_18):
        aged_over_18.click()

    @property
    def select_household_member(self):
        self.browser.find_element(*HouseholdHeadEligibilityPage.household_member).click()

    @property
    def select_aged_over_18_yes(self):
        return self.browser.find_element(*HouseholdHeadEligibilityPage.aged_over_18_yes)

    @property
    def select_aged_over_18_no(self):
        return self.browser.find_element(*HouseholdHeadEligibilityPage.aged_over_18_no)

    def set_household_residency(self, household_residency):
        household_residency.click()

    @property
    def select_household_residency_yes(self):
        return self.browser.find_element(*HouseholdHeadEligibilityPage.household_residency_yes)

    @property
    def select_household_residency_no(self):
        return self.browser.find_element(*HouseholdHeadEligibilityPage.household_residency_no)

    def set_verbal_script(self, verbal_script):
        verbal_script.click()

    @property
    def select_verbal_script_yes(self):
        return self.browser.find_element(*HouseholdHeadEligibilityPage.verbal_script_yes)

    @property
    def select_verbal_script_no(self):
        return self.browser.find_element(*HouseholdHeadEligibilityPage.verbal_script_no)

    def fill_representative_eligibility(self, aged_over_18, household_residency,
                                        verbal_script, report_date=None, report_time=None):
        if not report_date:
            self.click_report_today()
        else:
            self.set_report_date(report_date)

        if not report_time:
            self.click_report_now()
        else:
            self.set_report_time(report_time)

        self.select_household_member
        self.set_aged_over_18(aged_over_18)
        self.set_household_residency(household_residency)
        self.set_verbal_script(verbal_script)
        self.click_save_button()
