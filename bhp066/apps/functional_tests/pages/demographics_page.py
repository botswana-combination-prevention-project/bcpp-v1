from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class DemographicsPage(BaseModelAdminPage):
    religion = (By.ID, 'id_religion')
    ethnic = (By.ID, 'id_ethnic')
    marital_status = (By.ID, 'id_marital_status')
    live_with = (By.ID, 'id_live_with')

    def set_religion(self, religion):
        religion_element = self.browser.find_element(*DemographicsPage.religion)
        religion_element.send_keys(religion)

    def set_ethnic(self, ethnic):
        ethnic_element = self.browser.find_element(*DemographicsPage.ethnic)
        ethnic_element.send_keys(ethnic)

    def set_marital_status(self, marital_status):
        marital_status_element = self.browser.find_element(*DemographicsPage.marital_status)
        marital_status_element.send_keys(marital_status)

    def set_live_with(self, live_with):
        live_with_element = self.browser.find_element(*DemographicsPage.live_with)
        live_with_element.send_keys(live_with)

    def fill_demographic(self, religion, ethnic, marital_status, live_with):
        self.set_religion(religion)
        self.set_ethnic(ethnic)
        self.set_marital_status(marital_status)
        self.set_live_with(live_with)
        self.save_button()
