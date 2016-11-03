from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HouseholdHeadInfoPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_0')
    report_today = (By.XPATH, "(//form[@id='householdinfo_form']//descendant::a[text()='Today'])[1]")
    report_now = (By.XPATH, " (//form[@id='householdinfo_form']//descendant::a[text()='Now'])[1]")
    flooring_type = (By.ID, 'id_flooring_type')
    flooring_dirt = (By.ID, 'id_flooring_type_0')
    flooring_wood = (By.ID, 'id_flooring_type_1')
    flooring_tile = (By.ID, 'id_flooring_type_4')
    water_source = (By.ID, 'id_water_source')
    water_tap = (By.ID, 'id_water_source_0')
    water_piped = (By.ID, 'id_water_source_2')
    water_borehole = (By.ID, 'id_water_source_3')
    toilet_facility = (By.ID, 'id_toilet_facility')
    toilet_pitlatrine = (By.ID, 'id_toilet_facility_0')
    toilet_flush = (By.ID, 'id_toilet_facility_1')
    toilet_bush = (By.ID, 'id_toilet_facility_7')
    smaller_meals = (By.ID, 'id_smaller_meals')
    sm_meals_never = (By.ID, 'id_smaller_meals_0')
    sm_meals_rare = (By.ID, 'id_smaller_meals_1')
    sm_meals_sometime = (By.ID, 'id_smaller_meals_2')
    sm_meals_often = (By.ID, 'id_smaller_meals_3')
    sm_meals_no_ans = (By.ID, 'id_smaller_meals_4')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*HouseholdHeadInfoPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*HouseholdHeadInfoPage.report_time)
        time_element.send_keys(report_time)

    def click_report_today(self):
        self.browser.find_element(*HouseholdHeadInfoPage.report_today).click()

    def click_report_now(self):
        self.browser.find_element(*HouseholdHeadInfoPage.report_now).click()

    def set_flooring_type(self, flooring_type):
        flooring_type.click()

    @property
    def select_flooring_wood(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.flooring_wood)

    @property
    def select_flooring_tile(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.flooring_tile)

    @property
    def select_flooring_dirt(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.flooring_dirt)

    @property
    def select_water_tap(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.water_tap)

    @property
    def select_water_piped(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.water_piped)

    @property
    def select_water_borehole(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.water_borehole)

    def set_toilet_facility(self, toilet_facility):
        toilet_facility.click()

    @property
    def select_toilet_pitlatrine(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.toilet_pitlatrine)

    @property
    def select_toilet_flush(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.toilet_flush)

    @property
    def select_toilet_bush(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.toilet_bush)

    def set_small_meals(self, small_meals):
        small_meals.click()

    def select_sm_meals_never(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.sm_meals_never)

    def select_sm_meals_rare(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.sm_meals_rare)

    def select_sm_meals_sometime(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.sm_meals_sometime)

    def select_sm_meals_often(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.sm_meals_often)

    def select_sm_meals_no_ans(self):
        return self.browser.find_element(*HouseholdHeadInfoPage.sm_meals_no_ans)

    def fill_household_info(
        self, flooring_type, water_source, toilet_facility, smaller_meals, report_date=None, report_time=None
    ):
        if not report_date:
            self.click_report_today()
        else:
            self.set_report_date(report_date)
        if not report_time:
            self.click_report_now()
        else:
            self.set_report_time(report_time)
        self.set_flooring_type(flooring_type)
        self.toilet_facility(toilet_facility)
        self.smaller_meals(smaller_meals)
        self.click_save_button()
