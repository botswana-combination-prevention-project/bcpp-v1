from selenium.webdriver.common.by import By
from .base_page import BasePage


class PlotPage(BasePage):
    plot_status = (By.ID, 'id_status')
    non_res = (By.ID, 'id_status_0')
    res_non_habit = (By.ID, 'id_status_1')
    res_habit = (By.ID, 'id_status_2')
    inaccessible = (By.ID, 'id_status_3')
    gps_deg_south = (By.ID, 'id_gps_degrees_s')
    gps_min_south = (By.ID, 'ID_gps_minutes_s')
    gps_deg_east = (By.ID, 'id_gps_degree_e')
    gps_min_east = (By.ID, 'id_gps_minutes_e')
    household_count = (By.ID, 'id_household_count')
    time_of_week = (By.ID, 'id_time_of_week')
    time_of_day = (By.ID, 'id_time_of_day')
    save_button = (By.NAME, "_save")

    def set_plot_status(self, plot_status):
        plotElement = self.browser.find_element(*PlotPage.plot_status)
        plotElement.send_keys(plot_status)

    def set_deg_south(self, gps_deg_south):
        degsouthElement = self.browser.find_element(*PlotPage.gps_deg_south)
        degsouthElement.send_keys(gps_deg_south)

    def set_min_south(self, gps_min_south):
        degsouthElement = self.browser.find_element(*PlotPage.gps_min_south)
        degsouthElement.send_keys(gps_min_south)

    def set_deg_east(self, gps_deg_east):
        degeastElement = self.browser.find_element(*PlotPage.gps_deg_east)
        degeastElement.send_keys(gps_deg_east)

    def set_min_east(self, gps_min_east):
        minsouthElement = self.browser.find_element(*PlotPage.gps_min_east)
        minsouthElement.send_keys(gps_min_east)

    def set_household_count(self, household_count):
        HouseholdElement = self.browser.find_element(*PlotPage.household_count)
        HouseholdElement.send_keys(household_count)

    def click_save_button(self):
        self.browser.find_element(*PlotPage.save_button).click()

    def fill_plot_change(self, plot_status, gps_deg_south, gps_min_south, gps_deg_east, gps_min_east, household_count):
        self.set_plot_status(plot_status)
        self.set_deg_south(gps_deg_south)
        self.set_min_south(gps_min_south)
        self.set_deg_east(gps_deg_east)
        self.set_min_east(gps_min_east)
        self.set_household_count(household_count)
        self.click_save_button()
