from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotLogEntryPage(BasePage):
    report_date = (By.ID, 'report_datetime_0')
    report_time = (By.ID, 'report_datetime_1')
    plot_status = (By.ID, 'id_log_status_0')
    today = (By.XPATH, '')
    now = (By.XPATH, '')
    save_button = (By.XPATH, "//form[*/text()='Save']")

    def set_report_date(self, date):
        dateElement = self.browser.find_element(*PlotLogEntryPage.report_date)
        dateElement.send_keys(date)

    def set_report_time(self, time):
        dateElement = self.browser.find_element(*PlotLogEntryPage.report_time)
        dateElement.send_keys(time)

    def set_plot_status(self, plot_status):
        plotElement = self.browser.find_element(*PlotLogEntryPage.plot_status)
        plotElement.send_keys(plot_status)

    def click_today(self):
        self.browser.find_element(*PlotLogEntryPage.today).click()

    def click_save_button(self):
        self.browser.find_element(*PlotLogEntryPage.save_button).click()

    def fill_plot_log_entry(self, date, time, plot_status):
        self.set_report_date(date)
        self.set_report_time(time)
        self.set_plot_status(plot_status)
        self.click_save_button()
