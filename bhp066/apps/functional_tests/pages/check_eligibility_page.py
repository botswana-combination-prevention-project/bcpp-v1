from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class CheckEligibilityPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    report_today = (By.XPATH, "(//form[@id='enrollmentchecklist_form']//descendant::a[text()='Today'])[1]")
    report_now = (By.XPATH, " (//form[@id='enrollmentchecklist_form']//descendant::a[text()='Now'])[1]")
    initials = (By.ID, 'id_initials')
    dob = (By.ID, 'id_dob')
    dob_today = (By.XPATH, "(//form[@id='enrollmentchecklist_form']//descendant::a[text()='Today'])[2]")
    gender = (By.ID, 'id_gender')
    male = (By.ID, 'id_gender_0')
    female = (By.ID, 'id_gender_1')
    has_identity = (By.ID, 'id_has_identity')
    identity_yes = (By.ID, 'id_has_identity_0')
    identity_no = (By.ID, 'id_has_identity_1')
    citizen = (By.ID, 'id_citizen')
    citizen_yes = (By.ID, 'id_citizen_0')
    citizen_no = (By.ID, 'id_citizen_1')
    legal_marriage = (By.ID, 'id_legal_marriage')
    confirm_participation = (By.ID, 'confirm_participation')
    study_participation = (By.ID, 'id_study_participation')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*CheckEligibilityPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*CheckEligibilityPage.report_time)
        time_element.send_keys(report_time)

    def click_report_today(self):
        self.browser.find_element(*CheckEligibilityPage.report_today).click()

    def click_report_now(self):
        self.browser.find_element(*CheckEligibilityPage.report_now).click()

    def set_initials(self, initials):
        initials_element = self.browser.find_element(*CheckEligibilityPage.initials)
        initials_element.send_keys(initials)

    def set_dob(self, dob):
        dob_element = self.browser.find_element(*CheckEligibilityPage.dob)
        dob_element.send_keys(dob)

    def click_dob_today(self):
        self.browser.find_element(*CheckEligibilityPage.dob_today).click()

    def set_gender(self, gender):
        gender_element = self.browser.find_element(*CheckEligibilityPage.gender)
        gender_element.send_keys(gender)

    def select_male(self):
        self.browser.find_element(*CheckEligibilityPage.male).click()

    def select_female(self):
        self.browser.find_element(*CheckEligibilityPage.female).click()

    def set_has_identity(self, has_identity):
        has_identity_element = self.browser.find_element(*CheckEligibilityPage.has_identity)
        has_identity_element.send_keys(has_identity)

    def select_identity_yes(self):
        self.browser.find_element(*CheckEligibilityPage.identity_yes).click()

    def select_identity_no(self):
        self.browser.find_element(*CheckEligibilityPage.identity_no).click()

    def set_citizen(self, citizen):
        citizen_element = self.browser.find_element(*CheckEligibilityPage.citizen)
        citizen_element.send_keys(citizen)

    def select_citizen_yes(self):
        self.browser.find_element(*CheckEligibilityPage.citizen_yes).click()

    def select_citizen_no(self):
        self.browser.find_element(*CheckEligibilityPage.citizen_no).click()

    def set_legal_marriage(self, legal_marriage):
        legal_marriage_element = self.browser.find_element(*CheckEligibilityPage.legal_marriage)
        legal_marriage_element.send_keys(legal_marriage)

    def set_confirm_participation(self, confirm_participation):
        confirm_participation_element = self.browser.find_element(*CheckEligibilityPage.confirm_participation)
        confirm_participation_element.send_keys(confirm_participation)

    def set_study_participation(self, study_participation):
        study_participation_element = self.browser.find_element(*CheckEligibilityPage.study_participation)
        study_participation_element.send_keys(study_participation)

    def fill_check_eligibilty(self, report_date, report_time, dob, initials, gender, has_identity,
                              citizen, legal_marriage, confirm_participation, study_participation):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        if not dob:
            self.click_dob_today()
        else:
            self.set_dob(dob)
        self.set_initials(initials)
        self.set_gender(gender)
        self.set_has_identity(has_identity)
        self.set_citizen(citizen)
        self.set_legal_marriage(legal_marriage)
        self.set_confirm_participation(confirm_participation)
        self.set_study_participation(study_participation)
        self.click_save_button()
