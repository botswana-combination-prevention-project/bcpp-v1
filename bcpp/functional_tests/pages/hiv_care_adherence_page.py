from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HivCareAdeherencePage(BaseModelAdminPage):
    first_positive = (By.ID, 'id_first_positive')
    medical_care = (By.ID, 'id_medical_care')
    ever_recommended_arv = (By.ID, 'id_ever_recommend_arv')
    ever_taken_arv = (By.ID, 'id_ever_taken_arv')
    why_no_arv = (By.ID, 'id_why_no_arv')
    first_arv = (By.ID, 'id_first_arv')
    on_arv = (By.ID, 'id_on_arv')
    arv_evidence = (By.ID, 'id_arv_evidence')
    clinic_receiveing_from = (By.ID, 'id_clinic_receiving_from')
    next_appointment_date = (By.ID, 'id_next_appointment_date')
    arv_stop_date = (By.ID, 'id_arv_stop+date')
    arv_stop = (By.ID, 'id_arv_stop')
    adherence_4_day = (By.ID, 'id_adherence_4_day')
    adherence_4_wk = (By.ID, 'id_adherence_4_week')

    def set_first_positive(self, first_positive):
        first_positive_element = self.browser.find_element(*HivCareAdeherencePage.first_positive)
        first_positive_element.send_keys(first_positive)

    def set_medical_care(self, medical_care):
        medical_care_element = self.browser.find_element(*HivCareAdeherencePage.medical_care)
        medical_care_element.send_keys(medical_care)

    def set_ever_recommended_arv(self, ever_recommended_arv):
        ever_recommended_arv_element = self.browser.find_element(*HivCareAdeherencePage.ever_recommended_arv)
        ever_recommended_arv_element.send_keys(ever_recommended_arv)

    def set_ever_taken_arv(self, ever_taken_arv):
        ever_taken_arv_element = self.browser.find_element(*HivCareAdeherencePage.ever_taken_arv)
        ever_taken_arv_element.send_keys(ever_taken_arv)

    def set_why_no_arv(self, why_no_arv):
        why_no_arv_element = self.browser.find_element(*HivCareAdeherencePage.why_no_arv)
        why_no_arv_element.send_keys(why_no_arv)

    def set_first_arv(self, first_arv):
        first_arv_element = self.browser.find_element(*HivCareAdeherencePage.first_arv)
        first_arv_element.send_keys(first_arv)

    def set_on_arv(self, on_arv):
        on_arv_element = self.browser.find_element(*HivCareAdeherencePage.on_arv)
        on_arv_element.send_keys(on_arv)

    def set_arv_evidence(self, arv_evidence):
        arv_evidence_element = self.browser.find_element(*HivCareAdeherencePage.arv_evidence)
        arv_evidence_element.send_keys(arv_evidence)

    def set_clinic_receiveing_from(self, clinic_receiveing_from):
        clinic_receiveing_from_element = self.browser.find_element(*HivCareAdeherencePage.clinic_receiveing_from)
        clinic_receiveing_from_element.send_keys(clinic_receiveing_from)

    def set_next_appointment_date(self, next_appointment_date):
        next_appointment_date_element = self.browser.find_element(*HivCareAdeherencePage.next_appointment_date)
        next_appointment_date_element.send_keys(next_appointment_date)

    def set_arv_stop_date(self, arv_stop_date):
        arv_stop_date_element = self.browser.find_element(*HivCareAdeherencePage.arv_stop_date)
        arv_stop_date_element.send_keys(arv_stop_date)

    def set_arv_stop(self, arv_stop):
        arv_stop_element = self.browser.find_element(*HivCareAdeherencePage.arv_stop)
        arv_stop_element.send_keys(arv_stop)

    def set_adherence_4_day(self, adherence_4_day):
        adherence_4_day_element = self.browser.find_element(*HivCareAdeherencePage.adherence_4_day)
        adherence_4_day_element.send_keys(adherence_4_day)

    def set_adherence_4_wk(self, adherence_4_wk):
        adherence_4_wk_element = self.browser.find_element(*HivCareAdeherencePage.adherence_4_wk)
        adherence_4_wk_element.send_keys(adherence_4_wk)

    def fill_hiv_care_adherence(self, first_positive, medical_care, ever_recommended_arv, ever_taken_arv, why_no_arv,
                                first_arv, on_arv, arv_evidence, clinic_receiveing_from, next_appointment_date,
                                arv_stop_date, arv_stop, adherence_4_day, adherence_4_wk):
        self.set_first_positive(first_positive)
        self.set_medical_care(medical_care)
        self.set_ever_recommended_arv(ever_recommended_arv)
        self.set_ever_taken_arv(ever_taken_arv)
        self.set_why_no_arv(why_no_arv)
        self.set_arv_evidence(arv_evidence)
        self.set_clinic_receiveing_from(clinic_receiveing_from)
        self.set_next_appointment_date(next_appointment_date)
        self.set_arv_stop_date(arv_stop_date)
        self.set_arv_stop(arv_stop)
        self.set_adherence_4_day(adherence_4_day)
        self.set_adherence_4_wk(adherence_4_wk)
