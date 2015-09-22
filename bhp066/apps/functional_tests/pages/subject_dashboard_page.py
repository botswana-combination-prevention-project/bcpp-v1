from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage
from selenium.common.exceptions import NoSuchElementException


class SubjectDasbhoardPage(BaseModelAdminPage):
    link_name = ''
    new_subject_consent = (By.XPATH, ".//*[@id='left']/tbody/tr[1]/td/a")
    new_visit_link = (By.XPATH, ".//*[@id='left']/tbody/tr[2]/td/table/tbody/tr/td[6]/a")
    show_forms_link = (By.XPATH, ".//*[@id='left']/tbody/tr[2]/td/table/tbody/tr/td[8]/a")
    subject_locator_link = (By.XPATH, ".//*[@id='left']/tbody/tr[5]/td/table/tbody/tr[1]/td[3]/a")
    residency_and_mobility_link = (By.XPATH, ".//*[@id='left']/tbody/tr[5]/td/table/tbody/tr[2]/td[3]/a")
    residency_and_mobility_keyed = (By.XPATH, ".//*[@id='left']/tbody/tr[5]/td/table/tbody/tr[2]/td[4]/a")
    community_engagement_link = (By.XPATH, ".//*[@id='left']/tbody/tr[5]/td/table/tbody/tr[3]/td[3]/a")

    subject_dashboard_url ="http://localhost:8000/bcpp/dashboard/subject/household_member/1dfb8ee2-ab1e-4381-8ccb-44d6764e7a1f/appointments/"

    def click_new_subject_consent(self):
        self.browser.find_element(*SubjectDasbhoardPage.new_subject_consent).click()

    def click_new_visit_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.new_visit_link).click()

    def click_show_forms_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.subject_locator_link).click()

    def click_subject_locator_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.show_forms_link).click()

    def click_residency_mobility_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.residency_and_mobility_link).click()

    def click_community_engagement_link(self):
        self.browser.find_element(*SubjectDasbhoardPage.community_engagement_link).click()

    def is_show_forms_link_visible(self):
        try:
            return self.browser.find_element(*SubjectDasbhoardPage.show_forms_link).is_displayed()
        except NoSuchElementException:
            return False

    def is_residence_keyed_visible(self, residency_and_mobility_keyed):
        try:
            return self.browser.find_element(*SubjectDasbhoardPage.residency_and_mobility_keyed).is_displayed()
        except NoSuchElementException:
            return False
