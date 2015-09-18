from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotLogEntryPage(BasePage):
    report_date = (By.ID, 'report_datetime_0')
    report_time = (By.ID, 'report_datetime_1')
    plot_status = (By.ID, 'id_log_status_0')
    today = (By.XPATH, "//form[@id='plotlogentry_form']/descendant::a[text()='Today']")
    now = (By.XPATH, "//form[@id='plotlogentry_form']/descendant::a[text()='Now']")
    save_button = (By.NAME, "_save")

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

    def click_now(self):
        self.browser.find_element(*PlotLogEntryPage.now).click()

    def click_save_button(self):
        self.browser.find_element(*PlotLogEntryPage.save_button).click()

    def fill_plot_log_entry(self, date=None, time=None, plot_status):
        if not date:
            self.click_today()
        else:
            self.set_report_date(date)
        if not time:
            self.click_now()
        else:
            self.set_report_time(time)
        self.set_plot_status(plot_status)
        self.click_save_button()
