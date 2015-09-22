from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class SubjectLocatorPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    today = (By.XPATH, ".//*[@id='subjectlocator_form']/div/fieldset/div[2]/div/p/span[1]/a[1]")
    now = (By.XPATH, ".//*[@id='subjectlocator_form']/div/fieldset/div[2]/div/p/span[2]/a[1]")
    date_signed = (By.ID, 'id_date_signed')
    date_signed_today = (By.XPATH, ".//*[@id='subjectlocator_form']/div/fieldset/div[3]/div/span[2]/a[1]")
    home_visit_permission_yes = (By.ID, 'id_home_visit_permission_0')
    home_visit_permission_no = (By.ID, "id_home_visit_permission_1")
    may_follow_up_yes = (By.ID, 'id_may_follow_up_0')
    may_follow_up_no = (By.ID, 'id_may_follow_up_1')
    may_sms_follow_up_yes = (By.ID, 'id_may_sms_follow_up_0')
    may_sms_follow_up_no = (By.ID, 'id_may_sms_follow_up_1')
    may_call_work_yes = (By.ID, 'id_may_call_work_0')
    may_call_work_no = (By.ID, 'id_may_call_work_1')
    may_call_work_does_not_work = (By.ID, 'id_may_call_work_2')
    may_contact_someone_yes = (By.ID, 'id_may_contact_someone_0')
    may_contact_someone_no = (By.ID, 'id_may_contact_someone_1')
    has_alt_contact_yes = (By.ID, 'id_has_alt_contact_0')
    has_alt_contact_no = (By.ID, 'id_has_alt_contact_1')

    def set_report_date(self, date):
        date_element = self.browser.find_element(*SubjectLocatorPage.report_date)
        date_element.send_keys(date)

    def set_report_time(self, time):
        date_element = self.browser.find_element(*SubjectLocatorPage.report_time)
        date_element.send_keys(time)

    @property
    def select_today(self):
        self.browser.find_element(*SubjectLocatorPage.today).click()

    @property
    def select_now(self):
        self.browser.find_element(*SubjectLocatorPage.now).click()

    def set_date_signed(self, date_signed):
        date_element = self.browser.find_element(*SubjectLocatorPage.date_signed)
        date_element.send_keys(date_signed)

    @property
    def select_date_signed_today(self):
        self.browser.find_element(*SubjectLocatorPage.date_signed_today).click()

    @property
    def select_home_visit_permission_yes(self):
        return self.browser.find_element(*SubjectLocatorPage.home_visit_permission_yes)

    def set_home_visit_permission(self, home_visit_permission):
        home_visit_permission.click()

    @property
    def select_may_follow_up_yes(self):
        return self.browser.find_element(*SubjectLocatorPage.may_follow_up_yes)

    def set_may_follow_up(self, may_follow_up):
        may_follow_up.click()

    @property
    def select_may_sms_follow_up_yes(self):
        return self.browser.find_element(*SubjectLocatorPage.may_sms_follow_up_yes)

    def set_may_sms_follow_up(self, may_sms_follow_up):
        may_sms_follow_up.click()

    @property
    def select_may_call_work_yes(self):
        return self.browser.find_element(*SubjectLocatorPage.may_call_work_yes)

    def set_may_call_work(self, may_call_work):
        may_call_work.click()

    @property
    def select_may_contact_someone_yes(self):
        return self.browser.find_element(*SubjectLocatorPage.may_contact_someone_yes)

    def set_may_contact_someone(self, may_contact_someone):
        may_contact_someone.click()

    @property
    def select_has_alt_contact_yes(self):
        return self.browser.find_element(*SubjectLocatorPage.has_alt_contact_yes)

    def set_has_alt_contact(self, has_alt_contact):
        has_alt_contact.click()

    def fill_subject_locator(self, home_visit_permission, may_follow_up, may_sms_follow_up, may_call_work,
                             may_contact_someone, has_alt_contact, report_date=None, report_time=None,
                             date_signed=None):
        if not report_date:
            self.select_today
        else:
            self.set_report_date(report_date)
        if not report_time:
            self.select_now
        else:
            self.set_report_time(report_time)
        if not date_signed:
            self.select_date_signed_today
        else:
            self.set_date_signed(date_signed)
        self.set_home_visit_permission(home_visit_permission)
        self.set_may_follow_up(may_follow_up)
        self.set_may_sms_follow_up(may_sms_follow_up)
        self.set_may_call_work(may_call_work)
        self.set_may_contact_someone(may_contact_someone)
        self.set_has_alt_contact(has_alt_contact)
        self.click_save_button()
