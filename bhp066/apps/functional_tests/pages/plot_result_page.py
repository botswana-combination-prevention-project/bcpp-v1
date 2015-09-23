from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotResultPage(BasePage):
    add_new_entry = (By.XPATH, "//div/table/tbody/tr[1]/td[6]/ol/a")
    plot_id = "?"
    plot_link = (By.XPATH, '//div/table/tbody/tr[1]/td[1]/a')
    household = (By.XPATH, "//div[@class='results']/table/tbody/tr[1]/td[4]/descendant::input[@value='1 Household']")
    plot_log_entry_link = (By.XPATH, "//table/tbody/tr[1]/td[6]/ol/a[1]/li")
    action_status = (By.XPATH, ".//*[@id='result_list']/tbody/tr[1]/td[2]")

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

    def plot_log_entry_link_elem(self):
        return self.browser.find_element(*PlotResultPage.plot_log_entry_link)

    def action_status_elem(self):
        return self.browser.find_element(*PlotResultPage.action_status)
