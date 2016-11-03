from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class PlotLogEntryPage(BaseModelAdminPage):
    report_date = (By.ID, 'report_datetime_0')
    report_time = (By.ID, 'report_datetime_1')
    plot_status = (By.ID, 'id_log_status')
    accessible = (By.ID, 'id_log_status_0')
    inaccessible = (By.ID, 'id_log_status_1')
    today = (By.XPATH, ".//*[@id='plotlogentry_form']/div/fieldset/div[2]/div/p/span[1]/a[1]")
    now = (By.XPATH, ".//*[@id='plotlogentry_form']/div/fieldset/div[2]/div/p/span[2]/a[1]")

    def set_report_date(self, date):
        dateElement = self.browser.find_element(*PlotLogEntryPage.report_date)
        dateElement.send_keys(date)

    def set_report_time(self, time):
        dateElement = self.browser.find_element(*PlotLogEntryPage.report_time)
        dateElement.send_keys(time)

    def set_plot_status(self, plot_status):
        plot_status.click()

    @property
    def select_accessible(self):
        return self.browser.find_element(*PlotLogEntryPage.accessible)

    @property
    def select_inaccessible(self):
        return self.browser.find_element(*PlotLogEntryPage.inaccessible)

    @property
    def click_today(self):
        self.browser.find_element(*PlotLogEntryPage.today).click()

    @property
    def click_now(self):
        self.browser.find_element(*PlotLogEntryPage.now).click()

    @property
    def is_plot_log_entry(self):
        return self.browser.find_element(*PlotLogEntryPage.plot_status).is_displayed()

    def fill_plot_log_entry(self, plot_status, date=None, time=None):
        if not date:
            self.click_today
        else:
            self.set_report_date(date)
        if not time:
            self.click_now
        else:
            self.set_report_time(time)
        self.set_plot_status(plot_status)
        self.click_save_button()
