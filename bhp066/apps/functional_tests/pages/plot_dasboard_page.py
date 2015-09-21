from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotDashboardPage(BasePage):
    composition = (By.XPATH, "//div[@class='results']/table/tbody/tr[1]/td[3]/form/input[@type='submit' and @value='Composition']")

    def click_composition(self):
        self.browser.find_element(*PlotDashboardPage.composition).click()
