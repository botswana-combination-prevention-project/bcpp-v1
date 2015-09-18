from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectConsentPage(BaseModelAdminPage):
    first_name = (By.ID, 'id_first_name')
    last_name = (By.ID, 'id_last_name')
    initials = (By.ID, 'id_initials')
    language = (By.ID, 'id_language')
    en_language = (By.ID, 'id_language_1')
    is_literate = (By.ID, 'id_is_literate')
    literate = (By.ID, 'id_is_literate_0')
    not_literate = (By.ID, 'id_is_literate_1')
    consent_date = (By.ID, 'id_consent_datetime_0')
    consent_time = (By.ID, 'id_consent_datetime_1')
    gender = (By.ID, 'id_gender')
    dob = (By.ID, 'id_dob')
    is_dob_estimated = (By.ID, 'id_is_dob_estimated')
    citizen = (By.ID, 'id_citizen')
    identity = (By.ID, 'id_identity')
    confirm_identity = (By.ID, 'id_confirm_identity')
    may_store_samples = (By.ID, 'id_may_store_samples')
    consent_reviewed = (By.ID, 'id_consent_reviewed')
    study_questions = (By.ID, 'id_study_questions')
    assessment_score = (By.ID, 'id_assessment_score')
    consent_signature = (By.ID, 'id_consent_signature')
    consent_copy = (By.ID, 'id_consent_copy')

    def set_first_name(self, first_name):
        firstname_element = self.browser.find_element(*SubjectConsentPage.first_name)
        firstname_element.send_keys(first_name)

    def set_last_name(self, last_name):
        lastname_element = self.browser.find_element(*SubjectConsentPage.last_name)
        lastname_element.send_keys(last_name)

    def set_initials(self, initials):
        initials_element = self.browser.find_element(*SubjectConsentPage.initials)
        initials_element.send_keys(initials)

    def set_language(self, language):
        language_element = self.browser.find_element(*SubjectConsentPage.language)
        language_element.send_keys(language)

    def select_en_language(self):
        self.browser.find_element(*SubjectConsentPage.en_language)

    def set_is_literate(self, is_literate):
        language_element = self.browser.find_element(*SubjectConsentPage.is_literate)
        language_element.send_keys(is_literate)

    def select_literate(self):
        self.browser.find_element(*SubjectConsentPage.literate)

    def set_consent_date(self, consent_date):
        consentdate_element = self.browser.find_element(*SubjectConsentPage.consent_date)
        consentdate_element.send_keys(consent_date)

    def set_consent_time(self, consent_time):
        consenttime_element = self.browser.find_element(*SubjectConsentPage.consent_time)
        consenttime_element.send_keys(consent_time)

    def set_gender(self, gender):
        gender_element = self.browser.find_element(*SubjectConsentPage.gender)
        gender_element.send_keys(gender)

    def set_dob(self, dob):
        dob_element = self.browser.find_element(*SubjectConsentPage.dob)
        dob_element.send_keys(dob)

    def set_is_dob_estimated(self, is_dob_estimated):
        dobestimated_element = self.browser.find_element(*SubjectConsentPage.is_dob_estimated)
        dobestimated_element.send_keys(is_dob_estimated)

    def set_citizen(self, citizen):
        citizen_element = self.browser.find_element(*SubjectConsentPage.citizen)
        citizen_element.send_keys(citizen)

    def set_identity(self, identity):
        identity_element = self.browser.find_element(*SubjectConsentPage.identity)
        identity_element.send_keys(identity)

    def set_confirm_identity(self, confirm_identity):
        confirmidentity_element = self.browser.find_element(*SubjectConsentPage.confirm_identity)
        confirmidentity_element.send_keys(confirm_identity)

    def set_may_store_samples(self, may_store_samples):
        may_store_samples_element = self.browser.find_element(*SubjectConsentPage.may_store_samples)
        may_store_samples_element.send_keys(may_store_samples)

    def set_consent_reviewed(self, consent_reviewed):
        consent_reviewed_element = self.browser.find_element(*SubjectConsentPage.consent_reviewed)
        consent_reviewed_element.send_keys(consent_reviewed)

    def set_study_questions(self, study_questions):
        study_questions_element = self.browser.find_element(*SubjectConsentPage.study_questions)
        study_questions_element.send_keys(study_questions)

    def set_assessment_score(self, assessment_score):
        assessment_score_element = self.browser.find_element(*SubjectConsentPage.assessment_score)
        assessment_score_element.send_keys(assessment_score)

    def set_consent_signature(self, consent_signature):
        consent_signature_element = self.browser.find_element(*SubjectConsentPage.consent_signature)
        consent_signature_element.send_keys(consent_signature)

    def set_consent_copy(self, consent_copy):
        consent_copy_element = self.browser.find_element(*SubjectConsentPage.consent_copy)
        consent_copy_element.send_keys(consent_copy)

    def fill_consent(self, first_name, last_name, initials, language, is_literate, consent_date, consent_time,
                     gender, dob, is_dob_estimated, citizen, identity, confirm_identity, may_store_samples,
                     consent_reviewed, study_questions, assessment_score, consent_signature, consent_copy):
        self.first_name(first_name)
        self.last_name(last_name)
        self.initials(initials)
        self.language(language)
        self.is_literate(is_literate)
        self.consent_date(consent_date)
        self.consent_time(consent_time)
        self.gender(gender)
        self.dob(dob)
        self.is_dob_estimated(is_dob_estimated)
        self.citizen(citizen)
        self.identity(identity)
        self.confirm_identity(confirm_identity)
        self.may_store_samples(may_store_samples)
        self.consent_reviewed(consent_reviewed)
        self.study_questions(study_questions)
        self.assessment_score(assessment_score)
        self.consent_signature(consent_signature)
        self.consent_copy(consent_copy)
        self.click_save_button()
