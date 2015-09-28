from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class EducationPage(BaseModelAdminPage):
    education = (By.ID, 'id_education')
    no_job = (By.ID, 'id_job_description_0')
    farmer = (By.ID, 'id_job_description_1')
    domestic_worker = (By.ID, 'id_job_description_2')
    working = (By.ID, 'id_working')
    no_monthly_income = (By.ID, 'id_monthly_income_0')
    monthly_income_500_999 = (By.ID, 'id_monthly_income_2')

    @property
    def select_work_farmer(self):
        self.browser.find_element(*EducationPage.farmer).click()

    @property
    def select_salary_range_500_999(self):
        self.browser.find_element(*EducationPage.monthly_income_500_999).click()

    def set_education(self, education):
        education_element = self.browser.find_element(*EducationPage.education)
        education_element.send_keys(education)

    def set_working(self, working):
        working_element = self.browser.find_element(*EducationPage.working)
        working_element.send_keys(working)

    def fill_education(self, education=None, working=None):
        if education:
            self.set_education(education)
        else:
            self.select_work_farmer
        if working:
            self.set_working(working)
        else:
            self.select_salary_range_500_999
        self.save_button()
