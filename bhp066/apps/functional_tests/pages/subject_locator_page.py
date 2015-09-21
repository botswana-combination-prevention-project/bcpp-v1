from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectLocatorPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    date_signed = (By.ID, 'id_date_signed')
    home_visit_permission = (By.ID, 'id_home_visit_permission')
    may_follow_up = (By.ID, 'id_may_follow_up')
    may_sms_follow_up = (By.ID, 'id_may_sms_follow_up')
    may_call_work = (By.ID, 'id_may_call_work')
    may_contact_someone = (By.ID, 'id_may_contact_someone')
    has_alt_contact = (By.ID, 'id_has_alt_contact')

    def set_report_date(self, date):
        date_element = self.browser.find_element(*SubjectLocatorPage.report_date)
        date_element.send_keys(date)

    def set_report_time(self, time):
        date_element = self.browser.find_element(*SubjectLocatorPage.report_time)
        date_element.send_keys(time)

    def set_date_signed(self, date_signed):
        date_element = self.browser.find_element(*SubjectLocatorPage.date_signed)
        date_element.send_keys(date_signed)

    def set_home_visit_permission(self, home_visit_permission):
        homepermission_element = self.browser.find_element(*SubjectLocatorPage.home_visit_permission)
        homepermission_element.send_keys(home_visit_permission)

    def set_followup(self, may_follow_up):
        followup_element = self.browser.find_element(*SubjectLocatorPage.may_follow_up)
        followup_element.send_keys(may_follow_up)

    def set_sms_followup(self, may_sms_follow_up):
        sms_followup_element = self.browser.find_element(*SubjectLocatorPage.may_sms_follow_up)
        sms_followup_element.send_keys(may_sms_follow_up)

    def set_call_work(self, may_call_work):
        call_work_element = self.browser.find_element(*SubjectLocatorPage.may_call_work)
        call_work_element.send_keys(may_call_work)

    def set_contact_someone(self, may_contact_someone):
        contact_someone_element = self.browser.find_element(*SubjectLocatorPage.may_contact_someone)
        contact_someone_element.send_keys(may_contact_someone)

    def set_alt_contact(self, has_alt_contact):
        alt_contact_element = self.browser.find_element(*SubjectLocatorPage.has_alt_contact)
        alt_contact_element.send_keys(has_alt_contact)

    def fill_subject_locator(self, report_date, report_time, date_signed, home_visit_permission, may_follow_up,
                             may_sms_follow_up, may_call_work, may_contact_someone, has_alt_contact):
        self.set_report_date(report_date)
        self.report_time(report_time)
        self.date_signed(date_signed)
        self.home_visit_permission(home_visit_permission)
        self.may_follow_up(may_follow_up)
        self.may_sms_follow_up(may_sms_follow_up)
        self.may_call_work(may_call_work)
        self.may_contact_someone(may_contact_someone)
        self.has_alt_contact(has_alt_contact)
        self.save_button()
