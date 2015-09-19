from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class ResidencyMobilityPage(BaseModelAdminPage):
    length_residence = (By.ID, 'id_length_residence')
    permanent_resident = (By.ID, 'id_permanent_resident')
    intend_residency = (By.ID, 'id_intend_residency')
    nights_away = (By.ID, 'id_nights_away')
    cattle_postlands = (By.ID, 'id_cattle_postlands')

    def set_length_residence(self, length_residence):
        length_residence_element = self.browser.find_element(*ResidencyMobilityPage.length_residence)
        length_residence_element.send_keys(length_residence)

    def set_permanent_resident(self, permanent_resident):
        permanent_resident_element = self.browser.find_element(*ResidencyMobilityPage.permanent_resident)
        permanent_resident_element.send_keys(permanent_resident)

    def set_intend_residency(self, intend_residency):
        intend_residency_element = self.browser.find_element(*ResidencyMobilityPage.intend_residency)
        intend_residency_element.send_keys(intend_residency)

    def set_nights_away(self, nights_away):
        nights_away_element = self.browser.find_element(*ResidencyMobilityPage.nights_away)
        nights_away_element.send_keys(nights_away)

    def set_cattle_postlands(self, cattle_postlands):
        cattle_postlands_element = self.browser.find_element(*ResidencyMobilityPage.cattle_postlands)
        cattle_postlands_element.send_keys(cattle_postlands)

    def fill_residency_mobility(self, length_residence, permanent_resident, intend_residency, nights_away,
                                cattle_postlands):
        self.length_residence(length_residence)
        self.permanent_resident(permanent_resident)
        self.intend_residency(intend_residency)
        self.nights_away(nights_away)
        self.cattle_postlands(cattle_postlands)
        self.save_button
