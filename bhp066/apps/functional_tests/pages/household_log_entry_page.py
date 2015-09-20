from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HouseholdLogEntryPage(BaseModelAdminPage):

    report_date = (By.ID, 'id_report_datetime')
    today = (By.XPATH, "//form[@id='householdlogentry_form']/descendant::a[text()='Today']")
    household_status = (By.ID, 'id_household_status')
    eligible_present = (By.ID, 'id_household_status_0')
    eligible_absent = (By.ID, 'id_household_status_1')
    no_household_info = (By.ID, 'id_household_statu_2')
    refused_enum = (By.ID, 'id_household_status_3')
    next_appt_date = (By.ID, 'id_next_appt_datetime_0')
    next_appt_time = (By.ID, 'id_next_appt_datetime_1')
    next_appt_datetime_source = (By.ID, 'id_next_appt_datetime_source')
    no_source = (By.ID, 'id_next_appt_datetime_source_0')
    neighbour = (By.ID, 'id_next_appt_datetime_source_1')
    household_member = (By.ID, 'id_next_appt_datetime_source_2')
    field_ra = (By.ID, 'id_next_appt_datetime_source_3')
    other_source = (By.ID, 'id_next_appt_datetime_source_4')

    def set_household_status(self, household_status):
        household_status.click()

    @property
    def select_eligible_present(self):
        self.browser.find_element(*HouseholdLogEntryPage.eligible_present)

    @property
    def select_eeligible_absent(self):
        self.browser.find_element(*HouseholdLogEntryPage.eligible_absent)

    @property
    def select_no_household_info(self):
        self.browser.find_element(*HouseholdLogEntryPage.no_household_info)

    @property
    def select_refused_enum(self):
        self.browser.find_element(*HouseholdLogEntryPage.refused_enum)

    def set_report_date(self, report_date):
        dateElement = self.browser.find_element(*HouseholdLogEntryPage.report_date)
        dateElement.send_keys(report_date)

    def set_next_appt_date(self, next_appt_date):
        next_appt_date_element = self.browser.find_element(*HouseholdLogEntryPage.next_appt_date)
        next_appt_date_element.send_keys(next_appt_date)

    def set_next_appt_time(self, next_appt_time):
        next_appt_time_element = self.browser.find_element(*HouseholdLogEntryPage.next_appt_time)
        next_appt_time_element.send_keys(next_appt_time)

    @property
    def select_today(self):
        self.browser.find_element(*HouseholdLogEntryPage.today).click()

    def next_appt_datetime_source(self, next_source):
        next_source.click()

    @property
    def select_no_source(self):
        return self.browser.find_element(*HouseholdLogEntryPage.no_source)

    @property
    def select_neighbour(self):
        return self.browser.find_element(*HouseholdLogEntryPage.neighbour)

    @property
    def select_household_member(self):
        return self.browser.find_element(*HouseholdLogEntryPage.household_member)

    @property
    def select_field_ra(self):
        return self.browser.find_element(*HouseholdLogEntryPage.field_ra)

    @property
    def select_other_source(self):
        return self.browser.find_element(*HouseholdLogEntryPage.other_source)

    def fill_household_entry(self, household_status, report_date=None):
        if not report_date:
            self.select_today
        else:
            self.set_report_date(report_date)
        self.set_household_status(household_status)
        self.click_save()
