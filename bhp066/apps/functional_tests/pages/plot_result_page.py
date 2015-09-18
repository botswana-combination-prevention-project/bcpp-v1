from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotResultPage(BasePage):
    add_new_entry = (By.LINK_TEXT, 'add new entry')
    plot_id = "?"
    plot_link = (By.LINK_TEXT, plot_id)
    household = (By.XPATH, "//div[@class='results']/table/tbody/tr[1]/td[4]/descendant::input[@value='1 Households']")

    def click_addnewentry(self):
        self.browser.find_element(*PlotResultPage.add_new_entry).click()

    def set_plot_id(self, plot_id):
        self.plot_id = plot_id

    def click_plotlink(self):
        self.browser.find_element(*PlotResultPage.plot_link).click()

    def click_household(self):
        self.browser.find_element(*PlotResultPage.household).click()

    def get_plot(self, plot_id):
        self.set_plot_id(plot_id)
        self.click_plotlink()
