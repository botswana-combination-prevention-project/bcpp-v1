from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HouseholdMemberPage(BaseModelAdminPage):
    first_name = (By.ID, 'id_first_name')
    initials = (By.ID, 'id_initials')
    gender = (By.ID, 'id_gender')
    male = (By.ID, 'id_gender_0')
    female = (By.ID, 'id_gender_1')
    age_in_years = (By.ID, 'id_age_in_years')
    present_today = (By.ID, 'id_present_today')
    present_today_yes = (By.ID, 'id_present_today_0')
    present_today_no = (By.ID, 'id_present_today_1')
    inability_to_participate = (By.ID, 'id_inability_to_participate')
    can_participate = (By.ID, 'id_inability_to_participate_0')
    mental_incapacity = (By.ID, 'id_inability_to_participate_1')
    deaf_mute = (By.ID, 'id_inability_to_participate_2')
    too_sick = (By.ID, 'id_inability_to_participate_3')
    incarcerated = (By.ID, 'id_inability_to_participate_4')
    other_specify = (By.ID, 'id_inability_to_participate_5')
    study_resident = (By.ID, 'id_study_resident')
    study_resident_yes = (By.ID, 'id_study_resident_0')
    study_resident_no = (By.ID, 'id_study_resident_1')
    resident_dont_know = (By.ID, 'id_study_resident_2')
    relation = (By.ID, 'id_relation')
    relation_head = (By.ID, 'id_relation_0')
    relation_friend = (By.ID, 'id_relation_11')
    relation_partner = (By.ID, 'id_relation_28')
    save_button = (By.NAME, "_save")

    def set_first_name(self, first_name):
        firstnameElem = self.browser.find_element(*HouseholdMemberPage.first_name)
        firstnameElem.send_keys(first_name)

    def set_initials(self, initials):
        initialsElem = self.browser.find_element(*HouseholdMemberPage.initials)
        initialsElem.send_keys(initials)

    def set_gender(self, gender):
        gender.click()

    @property
    def select_male(self):
        return self.browser.find_element(*HouseholdMemberPage.male)

    @property
    def select_female(self):
        return self.browser.find_element(*HouseholdMemberPage.female)

    def set_age_in_years(self, age_in_years):
        age_element = self.browser.find_element(*HouseholdMemberPage.age_in_years)
        age_element.send_keys(age_in_years)

    def set_present_today(self, present_today):
        present_today.click()

    @property
    def select_present_today_yes(self):
        return self.browser.find_element(*HouseholdMemberPage.present_today_yes)

    @property
    def select_present_today_no(self):
        return self.browser.find_element(*HouseholdMemberPage.present_today_no)

    def set_inability_to_participate(self, inability_to_participate):
        inability_to_participate.click()

    @property
    def select_can_participate(self):
        return self.browser.find_element(*HouseholdMemberPage.can_participate)

    @property
    def select_mental_incapacity(self):
        return self.browser.find_element(*HouseholdMemberPage.mental_incapacity)

    @property
    def select_deaf_mute(self):
        return self.browser.find_element(*HouseholdMemberPage.deaf_mute)

    @property
    def select_too_sick(self):
        return self.browser.find_element(*HouseholdMemberPage.too_sick)

    @property
    def select_incarcerated(self):
        return self.browser.find_element(*HouseholdMemberPage.incarcerated)

    @property
    def select_other_specify(self):
        return self.browser.find_element(*HouseholdMemberPage.other_specify)

    def set_study_resident(self, study_resident):
        study_resident.click()

    @property
    def select_study_resident_yes(self):
        return self.browser.find_element(*HouseholdMemberPage.study_resident_yes)

    @property
    def select_study_resident_no(self):
        return self.browser.find_element(*HouseholdMemberPage.study_resident_no)

    @property
    def select_resident_dont_know(self):
        return self.browser.find_element(*HouseholdMemberPage.resident_dont_know)

    def set_relation(self, relation):
        relation.click()

    @property
    def select_head(self):
        return self.browser.find_element(*HouseholdMemberPage.relation_head)

    @property
    def select_friend(self):
        return self.browser.find_element(*HouseholdMemberPage.relation_friend)

    @property
    def select_partner(self):
        return self.browser.find_element(*HouseholdMemberPage.relation_partner)

    def fill_householdmember(self, first_name, initials, gender, age_in_years, present_today,
                             inability_to_participate, study_resident, relation):
        self.set_first_name(first_name)
        self.set_initials(initials)
        self.set_gender(gender)
        self.set_age_in_years(age_in_years)
        self.set_present_today(present_today)
        self.set_inability_to_participate(inability_to_participate)
        self.set_study_resident(study_resident)
        self.set_relation(relation)
        self.click_save_button()
