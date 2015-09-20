from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectConsentPage(BaseModelAdminPage):
    first_name = (By.ID, 'id_first_name')
    last_name = (By.ID, 'id_last_name')
    initials = (By.ID, 'id_initials')
    language = (By.ID, 'id_language')
    language_tn = (By.ID, 'id_language_0')
    language_en = (By.ID, 'id_language_1')
    language_kl = (By.ID, 'id_language_2')
    language_hm = (By.ID, 'id_language_3')
    is_literate = (By.ID, 'id_is_literate')
    is_literate_yes = (By.ID, 'id_is_literate_0')
    is_literate_no = (By.ID, 'id_is_literate_1')
    consent_date = (By.ID, 'id_consent_datetime_0')
    consent_time = (By.ID, 'id_consent_datetime_1')
    gender = (By.ID, 'id_gender')
    male = (By.ID, 'id_gender_0')
    female = (By.ID, 'id_gender_1')
    dob = (By.ID, 'id_dob')
    is_dob_estimated = (By.ID, 'id_is_dob_estimated')
    dob_estimated_no = (By.ID, 'id_is_dob_estimated_0')
    dob_estimated_day = (By.ID, 'id_is_dob_estimated_1')
    dob_estimated_month = (By.ID, 'id_is_dob_estimated_2')
    dob_estimated_year = (By.ID, 'id_is_dob_estimated_3')
    citizen = (By.ID, 'id_citizen')
    citizen_yes = (By.ID, 'id_citizen_yes')
    citizen_no = (By.ID, 'id_citizen_no')
    legal_marriage = (By.ID, 'id_legal_marriage')
    legal_marriage_yes = (By.ID, 'id_legal_marriage_0')
    legal_marriage_no = (By.ID, 'id_legal_marriage_1')
    legal_marriage_na = (By.ID, 'id_legal_marriage_2')
    legal_marriage = (By.ID, 'id_legal_marriage')
    legal_marriage_yes = (By.ID, 'id_legal_marriage_0')
    legal_marriage_no = (By.ID, 'id_legal_marriage_1')
    legal_marriage_na = (By.ID, 'id_legal_marriage_2')
    marriage_certificate = (By.ID, 'id_marriage_certificate')
    marriage_certificate_yes = (By.ID, 'id_marriage_certificate_0')
    marriage_certificate_no = (By.ID, 'id_marriage_certificate_1')
    marriage_certificate_na = (By.ID, 'id_marriage_certificate_2')
    identity = (By.ID, 'id_identity')
    identity_type = (By.ID, 'id_identity_type')
    identity_omang = (By.ID, 'id_identity_type_0')
    identity_drivers = (By.ID, 'id_identity_type_1')
    identity_passport = (By.ID, 'id_identity_type_2')
    identity_receipt = (By.ID, 'id_identity_type_3')
    confirm_identity = (By.ID, 'id_confirm_identity')
    may_store_samples = (By.ID, 'id_may_store_samples')
    store_samples_yes = (By.ID, 'id_may_store_samples_0')
    store_samples_no = (By.ID, 'id_may_store_samples_1')
    consent_reviewed = (By.ID, 'id_consent_reviewed')
    consent_reviewed_yes = (By.ID, 'id_consent_reviewed_0')
    consent_reviewed_no = (By.ID, 'id_consent_reviewed_1')
    study_questions = (By.ID, 'id_study_questions')
    study_questions_yes = (By.ID, 'id_study_questions_0')
    study_questions_no = (By.ID, 'id_study_questions_1')
    assessment_score = (By.ID, 'id_assessment_score')
    assessment_score_yes = (By.ID, 'id_assessment_score_0')
    assessment_score_no = (By.ID, 'id_assessment_score_1')
    consent_signature = (By.ID, 'id_consent_signature')
    consent_signature_yes = (By.ID, 'id_consent_signature_0')
    consent_signature_no = (By.ID, 'id_consent_signature_1')
    consent_copy = (By.ID, 'id_consent_copy')
    consent_copy_yes = (By.ID, 'id_consent_copy_0')
    consent_copy_no = (By.ID, 'id_consent_copy_1')

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
        language.click()

    @property
    def select_language_en(self):
        return self.browser.find_element(*SubjectConsentPage.language_en)

    @property
    def select_language_tn(self):
        return self.browser.find_element(*SubjectConsentPage.language_tn)

    @property
    def select_language_kl(self):
        return self.browser.find_element(*SubjectConsentPage.language_kl)

    @property
    def select_language_hm(self):
        return self.browser.find_element(*SubjectConsentPage.language_hm)

    def set_is_literate(self, is_literate):
        is_literate.click()

    @property
    def select_is_literate_yes(self):
        return self.browser.find_element(*SubjectConsentPage.is_literate_yes)

    @property
    def select_is_literate_no(self):
        return self.browser.find_element(*SubjectConsentPage.is_literate_no)

    def set_consent_date(self, consent_date):
        consentdate_element = self.browser.find_element(*SubjectConsentPage.consent_date)
        consentdate_element.send_keys(consent_date)

    def set_consent_time(self, consent_time):
        consenttime_element = self.browser.find_element(*SubjectConsentPage.consent_time)
        consenttime_element.send_keys(consent_time)

    def set_gender(self, gender):
        gender.click()

    @property
    def select_male(self):
        self.browser.find_element(*SubjectConsentPage.male)

    @property
    def select_female(self):
        self.browser.find_element(*SubjectConsentPage.female)

    def set_dob(self, dob):
        dob_element = self.browser.find_element(*SubjectConsentPage.dob)
        dob_element.send_keys(dob)

    def set_is_dob_estimated(self, is_dob_estimated):
        is_dob_estimated.click()

    @property
    def select_dob_estimated_no(self):
        self.browser.find_element(*SubjectConsentPage.dob_estimated_no)

    @property
    def select_dob_estimated_day(self):
        self.browser.find_element(*SubjectConsentPage.dob_estimated_day)

    @property
    def select_dob_estimated_month(self):
        self.browser.find_element(*SubjectConsentPage.dob_estimated_month)

    @property
    def select_dob_estimated_year(self):
        self.browser.find_element(*SubjectConsentPage.dob_estimated_year)

    def set_citizen(self, citizen):
        citizen.click()

    @property
    def select_citizen_yes(self):
        self.browser.find_element(*SubjectConsentPage.citizen_yes)

    @property
    def select_citizen_no(self):
        self.browser.find_element(*SubjectConsentPage.citizen_no)

    def set_legal_marriage(self, legal_marriage):
        legal_marriage.click()

    @property
    def select_legal_marriage_yes(self):
        return self.browser.find_element(*SubjectConsentPage.legal_marriage_yes)

    @property
    def select_legal_marriage_no(self):
        return self.browser.find_element(*SubjectConsentPage.legal_marriage_no)

    @property
    def select_legal_marriage_na(self):
        return self.browser.find_element(*SubjectConsentPage.legal_marriage_na)

    def set_marriage_certificate(self, marriage_certificate):
        marriage_certificate.click()

    @property
    def select_marriage_certificate_yes(self):
        return self.browser.find_element(*SubjectConsentPage.marriage_certificate_yes)

    @property
    def select_marriage_certificate_no(self):
        return self.browser.find_element(*SubjectConsentPage.marriage_certificate_no)

    @property
    def select_marriage_certificate_na(self):
        return self.browser.find_element(*SubjectConsentPage.marriage_certificate_na)

    def set_identity(self, identity):
        identity_element = self.browser.find_element(*SubjectConsentPage.identity)
        identity_element.send_keys(identity)

    def set_identity_type(self, identity_type):
        identity_type.click()

    @property
    def select_identity_omang(self):
        self.browser.find_element(*SubjectConsentPage.identity_omang)

    @property
    def select_identity_passport(self):
        self.browser.find_element(*SubjectConsentPage.identity_passport)

    @property
    def select_identity_drivers(self):
        self.browser.find_element(*SubjectConsentPage.identity_drivers)

    @property
    def select_identity_receipt(self):
        self.browser.find_element(*SubjectConsentPage.identity_receipt)

    def set_confirm_identity(self, confirm_identity):
        confirmidentity_element = self.browser.find_element(*SubjectConsentPage.confirm_identity)
        confirmidentity_element.send_keys(confirm_identity)

    def set_may_store_samples(self, may_store_samples):
        may_store_samples.click()

    @property
    def select_store_samples_yes(self):
        return self.browser.find_element(*SubjectConsentPage.store_samples_yes)

    @property
    def select_store_samples_no(self):
        return self.browser.find_element(*SubjectConsentPage.store_samples_no)

    def set_consent_reviewed(self, consent_reviewed):
        consent_reviewed.click()

    @property
    def select_consent_reviewed_yes(self):
        return self.browser.find_element(*SubjectConsentPage.consent_reviewed_yes)

    @property
    def select_consent_reviewed_no(self):
        return self.browser.find_element(*SubjectConsentPage.consent_reviewed_no)

    def set_study_questions(self, study_questions):
        study_questions.click()

    @property
    def select_study_questions_yes(self):
        return self.browser.find_element(*SubjectConsentPage.study_questions_yes)

    @property
    def select_study_questions_no(self):
        return self.browser.find_element(*SubjectConsentPage.study_questions_no)

    def set_assessment_score(self, assessment_score):
        assessment_score.click()

    @property
    def select_assessment_score_yes(self):
        return self.browser.find_element(*SubjectConsentPage.assessment_score_yes)

    @property
    def select_assessment_score_no(self):
        return self.browser.find_element(*SubjectConsentPage.assessment_score_no)

    def set_consent_signature(self, consent_signature):
        consent_signature.click()

    @property
    def select_consent_signature_yes(self):
        return self.browser.find_element(*SubjectConsentPage.consent_signature_yes)

    @property
    def select_consent_signature_no(self):
        return self.browser.find_element(*SubjectConsentPage.consent_signature_no)

    def set_consent_copy(self, consent_copy):
        consent_copy.click()

    @property
    def select_consent_copy_yes(self):
        return self.browser.find_element(*SubjectConsentPage.consent_copy_yes)

    @property
    def select_consent_copy_no(self):
        return self.browser.find_element(*SubjectConsentPage.consent_copy_no)

    def fill_consent(self, first_name, last_name, initials, language, is_literate, consent_date, consent_time,
                     gender, dob, is_dob_estimated, citizen, legal_marriage=select_legal_marriage_na,
                     marriage_certificate=select_marriage_certificate_na, identity, identity_type, confirm_identity,
                     may_store_samples, consent_reviewed, study_questions, assessment_score,
                     consent_signature, consent_copy):
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_initials(initials)
        self.set_language(language)
        self.set_is_literate(is_literate)
        self.set_consent_date(consent_date)
        self.set_consent_time(consent_time)
        self.set_gender(gender)
        self.set_dob(dob)
        self.set_is_dob_estimated(is_dob_estimated)
        self.set_citizen(citizen)
        self.set_legal_marriage(legal_marriage)
        self.set_marriage_certificate(marriage_certificate)
        self.set_identity(identity)
        self.set_identity_type(identity_type)
        self.set_confirm_identity(confirm_identity)
        self.set_may_store_samples(may_store_samples)
        self.set_consent_reviewed(consent_reviewed)
        self.set_study_questions(study_questions)
        self.set_assessment_score(assessment_score)
        self.set_consent_signature(consent_signature)
        self.set_consent_copy(consent_copy)
        self.set_click_save_button()
