from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage
from selenium.common.exceptions import NoSuchElementException


class SubjectDasbhoardPage(BaseModelAdminPage):
    new_subject_consent = (By.XPATH, ".//*[@id='left']/tbody/tr[1]/td/a")
    new_visit_link = (By.XPATH, ".//*[@id='left']/tbody/tr[2]/td/table/tbody/tr/td[6]/a")
    show_forms_link = (By.XPATH, ".//*[@id='left']/tbody/tr[2]/td/table/tbody/tr/td[8]/a")

    subject_dashboard_url ="http://localhost:8000/bcpp/dashboard/subject/visit/1ac500c6-bb5c-4ff1-b0ea-18f657a1dcb0/forms/"

    def click_new_subject_consent(self):
        self.browser.find_element(*SubjectDasbhoardPage.new_subject_consent).click()

    def click_new_visit_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.new_visit_link).click()

    def click_show_forms_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.show_forms_link).click()

    def is_show_forms_link_visible(self):
        try:
            return self.browser.find_element(*SubjectDasbhoardPage.show_forms_link).is_displayed()
        except NoSuchElementException:
            return False
