from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HouseholdMemberPage(BaseModelAdminPage):
    first_name = (By.ID, 'id_first_name')
    initials = (By.ID, 'id_initials')
    gender = (By.ID, 'id_gender')
    age_in_years = (By.ID, 'id_age_in_years')
    present_today = (By.ID, 'id_present_today')
    present = (By.ID, 'id_present_today_0')
    not_present = (By.ID, 'id_present_today_1')
    inability_to_participate = (By.ID, 'id_inability_to_participate')
    can_participate = (By.ID, 'id_inability_to_participate_0')
    study_resident = (By.ID, 'id_study_resident')
    is_resident = (By.ID, 'id_study_resident_0')
    relation = (By.ID, 'id_relation')
    relation_head = (By.ID, 'id_relation_0')
    save_button = (By.NAME, "_save")

    def set_first_name(self, first_name):
        firstnameElem = self.browser.find_element(*HouseholdMemberPage.first_name)
        firstnameElem.send_keys(first_name)

    def set_initials(self, initials):
        initialsElem = self.browser.find_element(*HouseholdMemberPage.initials)
        initialsElem.send_keys(initials)

    def set_gender(self, gender):
        gender_element = self.browser.find_element(*HouseholdMemberPage.gender)
        gender_element.send_keys(gender)

    def set_age_in_years(self, age_in_years):
        age_element = self.browser.find_element(*HouseholdMemberPage.age_in_years)
        age_element.send_keys(age_in_years)

    def set_present_today(self, present_today):
        present_today_element = self.browser.find_element(*HouseholdMemberPage.present_today)
        present_today_element.send_keys(present_today)

    def set_inability_to_participate(self, inability_to_participate):
        participate_element = self.browser.find_element(*HouseholdMemberPage.inability_to_participate)
        participate_element.send_keys(inability_to_participate)

    def select_can_participate(self):
        self.browser.find_element(*HouseholdMemberPage.can_participate).click()

    def set_study_resident(self, study_resident):
        resident_element = self.browser.find_element(*HouseholdMemberPage.study_resident)
        resident_element.send_keys(study_resident)

    def select_is_resident(self):
        self.browser.find_element(*HouseholdMemberPage.is_resident).click()

    def relation(self, relation):
        relation_element = self.browser.find_element(*HouseholdMemberPage.relation)
        relation_element.send_keys(relation)

    def select_head(self):
        self.browser.find_element(*HouseholdMemberPage.relation_head).click()

    def fill_householdmember(self, first_name, initials, gender, age_in_years,
                             inability_to_participate, present_today, relation, study_resident):
        self.set_first_name(first_name)
        self.set_initials(initials)
        self.set_gender(gender)
        self.set_age_in_years(age_in_years)
        self.set_inability_to_participate(inability_to_participate)
        self.set_present_today(present_today)
        self.relation(relation)
        self.set_study_resident(study_resident)
        self.click_save()
