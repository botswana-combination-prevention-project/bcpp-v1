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
    legal_marriage_yes = (By.ID, 'id_legal_marriage_0')
    legal_marriage_no = (By.ID, 'id_legal_marriage_1')
    legal_marriage_na = (By.ID, 'id_legal_marriage_2')
    study_participation = (By.ID, 'id_study_participation')
    study_participation_yes = (By.ID, 'id_study_participation_0')
    study_participation_no = (By.ID, 'id_study_participation_1')
    confirm_participation = (By.ID, 'confirm_participation')
    confirm_participation_yes = (By.ID, 'confirm_participation_0')
    confirm_participation_no = (By.ID, 'confirm_participation_1')
    confirm_participation_na = (By.ID, 'confirm_participation_2')
    marriage_certificate = (By.ID, 'id_marriage_certificate')
    marriage_certificate_yes = (By.ID, 'id_marriage_certificate_0')
    marriage_certificate_no = (By.ID, 'id_marriage_certificate_1')
    part_time_resident = (By.ID, 'id_part_time_resident')
    part_time_resident_yes = (By.ID, 'id_part_time_resident_0')
    part_time_resident_no = (By.ID, 'id_part_time_resident_1')
    household_residency = (By.ID, 'id_household_residency')
    household_residency_yes = (By.ID, 'id_household_residency_yes')
    household_residency_no = (By.ID, 'id_household_residency_no')
    literacy = (By.ID, 'id_literacy')
    literacy_yes = (By.ID, 'id_literacy_0')
    literacy_no = (By.ID, 'id_literacy_1')
    guardian = (By.ID, 'id_guardian')
    guardian_yes = (By.ID, 'id_guardian_yes')
    guardian_no = (By.ID, 'id_guardian_no')
    guardian_na = (By.ID, 'id_guardian_na')

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
        gender.click()

    @property
    def select_male(self):
        return self.browser.find_element(*CheckEligibilityPage.male)

    @property
    def select_female(self):
        return self.browser.find_element(*CheckEligibilityPage.female)

    def set_has_identity(self, has_identity):
        has_identity.click()

    @property
    def select_identity_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.identity_yes)

    @property
    def select_identity_no(self):
        return self.browser.find_element(*CheckEligibilityPage.identity_no)

    def set_citizen(self, citizen):
        citizen.click()

    @property
    def select_citizen_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.citizen_yes)

    @property
    def select_citizen_no(self):
        return self.browser.find_element(*CheckEligibilityPage.citizen_no)

    def set_legal_marriage(self, legal_marriage):
        legal_marriage.click()

    @property
    def select_legal_marriage_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.legal_marriage_yes)

    @property
    def select_legal_marriage_no(self):
        return self.browser.find_element(*CheckEligibilityPage.legal_marriage_no)

    @property
    def select_legal_marriage_na(self):
        return self.browser.find_element(*CheckEligibilityPage.legal_marriage_na)

    def set_study_participation(self, study_participation):
        study_participation.click()

    @property
    def select_study_participation_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.study_participation_yes)

    @property
    def select_study_participation_no(self):
        return self.browser.find_element(*CheckEligibilityPage.study_participation_no)

    def set_confirm_participation(self, confirm_participation):
        confirm_participation.click()

    @property
    def select_confirm_participation_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.confirm_participation_yes)

    @property
    def select_confirm_participation_no(self):
        return self.browser.find_element(*CheckEligibilityPage.confirm_participation_no)

    @property
    def select_confirm_participation_na(self):
        return self.browser.find_element(*CheckEligibilityPage.confirm_participation_na)

    def set_marriage_certificate(self, marriage_certificate):
        marriage_certificate.click()

    @property
    def select_marriage_certificate_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.marriage_certificate_yes)

    @property
    def select_marriage_certificate_no(self):
        return self.browser.find_element(*CheckEligibilityPage.marriage_certificate_no)

    @property
    def select_marriage_certificate_na(self):
        return self.browser.find_element(*CheckEligibilityPage.marriage_certificate_na)

    def set_part_time_resident(self, part_time_resident):
        part_time_resident.click()

    @property
    def select_part_time_resident_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.part_time_resident_yes)

    @property
    def select_part_time_resident_no(self):
        return self.browser.find_element(*CheckEligibilityPage.part_time_resident_no)

    def set_household_residency(self, household_residency):
        household_residency.click()

    @property
    def select_household_residencyt_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.household_residency_yes)

    @property
    def select_household_residency_no(self):
        return self.browser.find_element(*CheckEligibilityPage.household_residency_no)

    def set_literacy(self, literacy):
        literacy.click()

    @property
    def select_literacy_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.literacy_yes)

    @property
    def select_literacy_no(self):
        return self.browser.find_element(*CheckEligibilityPage.literacy_no)

    def set_guardian(self, guardian):
        guardian.click()

    @property
    def select_guardian_yes(self):
        return self.browser.find_element(*CheckEligibilityPage.guardian)

    @property
    def select_guardian_no(self):
        return self.browser.find_element(*CheckEligibilityPage.guardian)

    @property
    def select_guardian_na(self):
        return self.browser.find_element(*CheckEligibilityPage.guardian)

    def fill_check_eligibilty(
            self, dob, initials, gender, has_identity,
            citizen, study_participation, marriage_certificate, part_time_resident,
            household_residency, literacy, guardian=select_guardian_na, confirm_participation=select_confirm_participation_na,
            legal_marriage=select_legal_marriage_na):

        self.click_report_today()
        self.click_report_now()
        if not dob:
            self.click_dob_today()
        else:
            dob = '1990-09-20'
            self.set_dob(dob)
        self.set_initials(initials)
        self.set_gender(gender)
        self.set_has_identity(has_identity)
        self.set_citizen(citizen)
        self.set_legal_marriage(legal_marriage)
        self.set_study_participation(study_participation)
        self.set_confirm_participation(confirm_participation)
        self.set_marriage_certificate(marriage_certificate)
        self.set_part_time_resident(part_time_resident)
        self.household_residency(household_residency)
        self.literacy(literacy)
        self.guardian(guardian)
        self.click_save_button()
