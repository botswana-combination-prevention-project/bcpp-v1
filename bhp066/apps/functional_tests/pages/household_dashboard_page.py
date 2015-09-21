from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.common.exceptions import NoSuchElementException


class HouseholdDashboardPage(BasePage):
    household_log_entry = (By.XPATH, "//div[@id='tile_wrapper']/p[2]/a")
    household_member = (By.XPATH, "//div[@id='tile_wrapper']/table[3]/tbody/tr/td/a")
    check_eligibility = (By.LINK_TEXT, 'Check eligibility')
    subject_dashboard = (By.XPATH, "//div/table[2]/tbody/tr[1]/td[9]/ol/li[2]/a")
    fill_representative_link = (By.XPATH, "//div[@id='tile_wrapper']/p[3]/a[text()='Fill Representative Eligibility form to continue']")
    hod_eligibility_checklist_link = (By.XPATH, "//div[@id='tile_wrapper']/p[3]/a[text()='Head of Household Eligibility Checklist']")
    household_info_link = (By.XPATH, ".//*[@id='tile_wrapper']/p[3]/a")

    def click_add_househouldentry(self):
        self.browser.find_element(*HouseholdDashboardPage.household_log_entry).click()

    def click_add_householdmember(self):
        self.browser.find_element(*HouseholdDashboardPage.household_member).click()

    def click_check_eligibility(self):
        self.browser.find_element(*HouseholdDashboardPage.check_eligibility).click()

    def click_subject_consent(self):
        self.browser.find_element(*HouseholdDashboardPage.subject_dashboard).click()

    @property
    def click_fill_representative(self):
        try:
            self.browser.find_element(*HouseholdDashboardPage.fill_representative_link).click()
            return True
        except NoSuchElementException:
            return False

    @property
    def click_hod_eligibility_checklist_link(self):
        try:
            self.browser.find_element(*HouseholdDashboardPage.hod_eligibility_checklist_link).click()
            return True
        except NoSuchElementException:
            return False

    @property
    def click_household_info_link(self):
        try:
            self.browser.find_element(*HouseholdDashboardPage.household_info_link).click()
            return True
        except NoSuchElementException:
            return False

    @property
    def click_household_info_link_visible(self):
        return self.browser.find_element(*HouseholdDashboardPage.household_info_link).is_displayed()

    @property
    def is_fill_representative_link_visible(self):
        try:
            return self.browser.find_element(*HouseholdDashboardPage.fill_representative_link).is_displayed()
        except NoSuchElementException:
            return False

    @property
    def is_fill_representative_link_text(self):
        self.browser.find_element(*HouseholdDashboardPage.fill_representative_link).text
