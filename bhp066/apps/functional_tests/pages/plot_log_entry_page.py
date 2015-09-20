from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class PlotLogEntryPage(BaseModelAdminPage):
    report_date = (By.ID, 'report_datetime_0')
    report_time = (By.ID, 'report_datetime_1')
    plot_status = (By.ID, 'id_log_status')
    accessible = (By.ID, 'id_log_status_0')
    inaccessible = (By.ID, 'id_log_status_1')
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

    @property
    def select_accessible(self):
        self.browser.find_element(*PlotLogEntryPage.accessible).click()

    @property
    def select_inaccessible(self):
        self.browser.find_element(*PlotLogEntryPage.inaccessible).click()

    def click_today(self):
        self.browser.find_element(*PlotLogEntryPage.today).click()

    def click_now(self):
        self.browser.find_element(*PlotLogEntryPage.now).click()

    def fill_plot_log_entry(self, date=None, time=None, plot_status=None):
        if not date:
            self.click_today()
        else:
            self.set_report_date(date)
        if not time:
            self.click_now()
        else:
            self.set_report_time(time)
        if not plot_status:
            self.set_plot_status(plot_status)
        else:
            self.select_accessible()
        self.click_save_button()
