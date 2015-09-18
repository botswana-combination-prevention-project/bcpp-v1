from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotDashboardPage(BasePage):
    composition = (By.XPATH, "//tr[@class='row1']/td/form/input[@value='Composition']")

    def click_composition(self, plot_status):
        compositionElement = self.browser.find_element(*HouseholdDashboardPage.composition)
        compositionElement.send_keys(plot_status)
