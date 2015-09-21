from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectDasbhoardPage(BaseModelAdminPage):
    new_subject_consent = (By.LINK_TEXT, 'subject consent (new)')

    def click_new_subject_consent(self):
        self.browser.find_element(*SubjectDasbhoardPage.new_subject_consent).click()
