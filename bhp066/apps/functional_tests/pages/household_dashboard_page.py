from selenium.webdriver.common.by import By
from .base_page import BasePage


class HouseholdDashboardPage(BasePage):
    household_log_entry = (By.LINK_TEXT, "Add a household log entry")

    def click_addhousehouldentry(self, household_log_entry):
        self.browser.find_element(*HouseholdDashboardPage.household_log_entry).click()
