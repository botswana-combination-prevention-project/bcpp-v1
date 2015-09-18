from selenium.webdriver.common.by import By
from .base_page import BasePage


class HouseholdDashboardPage(BasePage):
    household_log_entry = (By.LINK_TEXT, "Add a household log entry")
    household_member = (By.LINK_TEXT, 'Add another household member')
    check_eligibility = (By.LINK_TEXT, 'Check eligibility')
    subject_dashboard = (By.XPATH, "//div/table[2]/tbody/tr[1]/td[9]/ol/li[2]/a")

    def click_add_househouldentry(self):
        self.browser.find_element(*HouseholdDashboardPage.household_log_entry).click()

    def click_add_householdmember(self):
        self.browser.find_element(*HouseholdDashboardPage.household_member).click()

    def click_check_eligibility(self):
        self.browser.find_element(*HouseholdDashboardPage.check_eligibility).click()

    def click_subject_consent(self):
        self.browser.find_element(*HouseholdDashboardPage.subject_dashboard).click()
