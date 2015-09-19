from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class EducationPage(BaseModelAdminPage):
    education = (By.ID, 'id_education')
    working = (By.ID, 'id_working')

    def set_education(self, education):
        education_element = self.browser.find_element(*EducationPage.education)
        education_element.send_keys(education)

    def set_working(self, working):
        working_element = self.browser.find_element(*EducationPage.working)
        working_element.send_keys(working)

    def fill_education(self, education, working):
        self.set_education(education)
        self.set_working(working)
        self.save_button()
