from selenium.webdriver.common.by import By
from .base_page import BasePage


class HouseholdDashboardPage(BasePage):
    composition = (By.XPATH, 'id_status')

    def click_composition(self, plot_status):
        plotElement = self.browser.find_element(*HouseholdDashboardPage.plot_status)
        plotElement.send_keys(plot_status)
