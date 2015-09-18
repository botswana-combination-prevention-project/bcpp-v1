from selenium.webdriver.common.by import By
from .base_page import BasePage


class HouseholdDashboardPage(BasePage):
    household_log_entry = (By.LINK_TEXT, "Add a household log entry")
    household_member = (By.LINK_TEXT, 'Add another household member')

    def click_add_househouldentry(self, household_log_entry):
        self.browser.find_element(*HouseholdDashboardPage.household_log_entry).click()

    def click_add_householdmember(self):
        self.browser.find_element(*HouseholdDashboardPage.household_member).click()
