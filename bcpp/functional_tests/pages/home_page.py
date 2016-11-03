from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    plot_button = (By.NAME, 'plot')
    household_button = (By.NAME, 'household')
    member_button = (By.NAME, 'member')
    subject_button = (By.NAME, 'subject')
    reports_button = (By.NAME, 'reports')
    analytics_button = (By.NAME, 'Analytics')
    admin_button = (By.NAME, 'administration')

    def click_plot(self):
        self.browser.find_element(*HomePage.plot_button).click()
