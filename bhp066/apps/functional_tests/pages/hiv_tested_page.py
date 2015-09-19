from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class HivTestedPage(BaseModelAdminPage):
    num_hiv_tests = (By.ID, 'id_num_hiv_tests')
    where_hiv_test = (By.ID, 'id_where_hiv_test')
    why_hiv_test = (By.ID, 'id_why_hiv_test')
    hiv_pills = (By.ID, 'id_hiv_pills')

    def set_num_hiv_tests(self, num_hiv_tests):
        num_hiv_tests_element = self.browser.find_element(*HivTestedPage.num_hiv_tests)
        num_hiv_tests_element.send_keys(num_hiv_tests)

    def set_where_hiv_test(self, where_hiv_test):
        where_hiv_test_element = self.browser.find_element(*HivTestedPage.where_hiv_test)
        where_hiv_test_element.send_keys(where_hiv_test)

    def set_why_hiv_test(self, why_hiv_test):
        why_hiv_test_element = self.browser.find_element(*HivTestedPage.why_hiv_test)
        why_hiv_test_element.send_keys(why_hiv_test)

    def set_hiv_pills(self, hiv_pills):
        hiv_pills_element = self.browser.find_element(*HivTestedPage.hiv_pills)
        hiv_pills_element.send_keys(hiv_pills)

    def fill_hiv_tested(self, num_hiv_tests, where_hiv_test, why_hiv_test, hiv_pills):
        self.num_hiv_tests(num_hiv_tests)
        self.where_hiv_test(where_hiv_test)
        self.why_hiv_test(why_hiv_test)
        self.hiv_pills(hiv_pills)
        self.save_button()
