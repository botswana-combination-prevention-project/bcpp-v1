from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotDashboardPage(BasePage):
    composition = (By.XPATH, "(//form[@id='householdlogentry_form']//descendant::a[text()='Today'])[1]")

    def click_composition(self, plot_status):
        compositionElement = self.browser.find_element(*PlotDashboardPage.composition)
        compositionElement.send_keys(plot_status)
