from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class ResidencyMobilityPage(BaseModelAdminPage):
    length_residence = (By.ID, 'id_length_residence')
    length_month_6 = (By.ID, 'id_length_residence_0')
    length_month_6_12 = (By.ID, 'id_length_residence_1')
    length_year_1_5 = (By.ID, 'id_length_residence_2')
    permanent_resident = (By.ID, 'id_permanent_resident')
    permanent_resident_yes = (By.ID, 'id_permanent_resident_0')
    permanent_resident_no = (By.ID, 'id_permanent_resident_1')
    intend_residency = (By.ID, 'id_intend_residency')
    intend_residency_yes = (By.ID, 'id_intend_residency_0')
    intend_residency_no = (By.ID, 'id_intend_residency_1')
    nights_away = (By.ID, 'id_nights_away')
    nights_away_0 = (By.ID, 'id_nights_away_0')
    nights_away_nt_6 = (By.ID, 'id_nights_away_1')
    nights_away_wk2 = (By.ID, 'id_nights_away_2')
    nights_away_wk3 = (By.ID, 'id_nights_away_3')
    cattle_postlands = (By.ID, 'id_cattle_postlands')
    cattle_postlands_na = (By.ID, 'id_cattle_postlands_0')
    cattle_postlands_farm = (By.ID, 'id_cattle_postlands_1')
    cattle_postlands_cattle = (By.ID, 'id_cattle_postlands_2')

    def set_length_residence(self, length_residence):
        length_residence.click()

    @property
    def select_length_month_6(self):
        return self.browser.find_element(*ResidencyMobilityPage.length_month_6)

    @property
    def select_length_month_6_12(self):
        return self.browser.find_element(*ResidencyMobilityPage.length_month_6_12)

    @property
    def select_length_year_1_5(self):
        return self.browser.find_element(*ResidencyMobilityPage.length_year_1_5)

    def set_permanent_resident(self, permanent_resident):
        permanent_resident.click()

    @property
    def select_permanent_resident_yes(self):
        return self.browser.find_element(*ResidencyMobilityPage.permanent_resident_yes)

    @property
    def select_permanent_resident_no(self):
        return self.browser.find_element(*ResidencyMobilityPage.permanent_resident_no)

    def set_intend_residency(self, intend_residency):
        intend_residency.click()

    @property
    def select_intend_residency_yes(self):
        return self.browser.find_element(*ResidencyMobilityPage.intend_residency_yes)

    @property
    def select_intend_residency_no(self):
        return self.browser.find_element(*ResidencyMobilityPage.intend_residency_no)

    def set_nights_away(self, nights_away):
        nights_away.click()

    @property
    def select_nights_away_0(self):
        return self.browser.find_element(*ResidencyMobilityPage.nights_away_0)

    @property
    def select_nights_away_nt_6(self):
        return self.browser.find_element(*ResidencyMobilityPage.nights_away_nt_6)

    @property
    def select_nights_away_wk2(self):
        return self.browser.find_element(*ResidencyMobilityPage.nights_away_wk2)

    @property
    def select_nights_away_wk3(self):
        return self.browser.find_element(*ResidencyMobilityPage.nights_away_wk3)

    def set_cattle_postlands(self, cattle_postlands):
        cattle_postlands.click()

    @property
    def select_cattle_postlands_na(self):
        return self.browser.find_element(*ResidencyMobilityPage.cattle_postlands_na)

    @property
    def select_cattle_postlands_farm(self):
        return self.browser.find_element(*ResidencyMobilityPage.cattle_postlands_farm)

    @property
    def select_cattle_postlands_cattle(self):
        return self.browser.find_element(*ResidencyMobilityPage.cattle_postlands_cattle)

    def fill_residency_mobility(self, length_residence, permanent_resident, intend_residency, nights_away,
                                cattle_postlands):
        self.set_length_residence(length_residence)
        self.set_permanent_resident(permanent_resident)
        self.set_intend_residency(intend_residency)
        self.set_nights_away(nights_away)
        self.set_cattle_postlands(cattle_postlands)
        self.click_save_button()
