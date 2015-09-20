from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class PlotPage(BaseModelAdminPage):
    plot_status = (By.ID, 'id_status')
    non_residential = (By.ID, 'id_status_0')
    res_non_habit = (By.ID, 'id_status_1')
    res_habit = (By.ID, 'id_status_2')
    inaccessible = (By.ID, 'id_status_3')
    gps_deg_south = (By.ID, 'id_gps_degrees_s')
    gps_min_south = (By.ID, 'id_gps_minutes_s')
    gps_deg_east = (By.ID, 'id_gps_degree_e')
    gps_min_east = (By.ID, 'id_gps_minutes_e')
    household_count = (By.ID, 'id_household_count')
    time_of_week = (By.ID, 'id_time_of_week')
    no_time_of_week = (By.ID, 'id_time_of_week_0')
    weekdays = (By.ID, 'id_time_of_week_1')
    weekends = (By.ID, 'id_time_of_week_2')
    time_of_day = (By.ID, 'id_time_of_day')
    no_time_of_day = (By.ID, 'id_time_of_day_0')
    morning = (By.ID, 'id_time_of_day_1')
    afternoon = (By.ID, 'id_time_of_day_2')
    evening = (By.ID, 'id_time_of_day_3')

    def set_plot_status(self, plot_status):
        plot_status.click()

    @property
    def select_non_residential(self):
        return self.browser.find_element(*PlotPage.non_residential)

    @property
    def select_res_non_habit(self):
        return self.browser.find_element(*PlotPage.res_non_habit)

    @property
    def select_res_habit(self):
        return self.browser.find_element(*PlotPage.res_habit)

    @property
    def select_inaccessible(self):
        return self.browser.find_element(*PlotPage.inaccessible)

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

    def set_time_of_week(self, time_of_week):
        time_of_week.click()

    @property
    def select_no_time_of_week(self):
        return self.browser.find_element(*PlotPage.no_time_of_week)

    @property
    def select_weekdays(self):
        return self.browser.find_element(*PlotPage.weekdays)

    @property
    def select_weekends(self):
        return self.browser.find_element(*PlotPage.weekends)

    def set_time_of_day(self, time_of_day):
        time_of_day.click()

    @property
    def select_no_time_of_day(self):
        return self.browser.find_element(*PlotPage.no_time_of_day)

    @property
    def select_morning(self):
        return self.browser.find_element(*PlotPage.morning)

    @property
    def select_afternoon(self):
        return self.browser.find_element(*PlotPage.afternoon)

    @property
    def select_evening(self):
        return self.browser.find_element(*PlotPage.evening)

    def fill_plot_change(self, plot_status, gps_deg_south, gps_min_south, gps_deg_east, gps_min_east, household_count,
                         time_of_week, time_of_day):
        self.set_plot_status(plot_status)
        self.set_deg_south(gps_deg_south)
        self.set_min_south(gps_min_south)
        self.set_deg_east(gps_deg_east)
        self.set_min_east(gps_min_east)
        self.set_household_count(household_count)
        self.set_time_of_week(time_of_week)
        self.set_time_of_day(time_of_day)
        self.click_save_button()
