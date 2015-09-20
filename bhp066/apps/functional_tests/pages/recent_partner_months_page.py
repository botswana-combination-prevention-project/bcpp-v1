from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class RecentPartnerPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    first_partner_live = (By.ID, 'id_first_partner_live')
    sex_partner_community = (By.ID, 'id_sex_partner_community')
    past_year_sex_freq = (By.ID, 'id_past_year_sex_freq')
    third_last_sex = (By.ID, 'id_third_last_sex')
    first_first_sex = (By.ID, 'id_first_first_sex')
    first_sex_current = (By.ID, 'id_first_sex_current')
    first_relationship = (By.ID, 'id_first_relationship')
    first_exchange = (By.ID, 'id_first_exchange')
    concurrent = (By.ID, 'id_concurrent')
    goods_exchange = (By.ID, 'id_goods_exchange')
    first_sex_freq = (By.ID, 'id_first_sex_freq')
    first_partner_hiv = (By.ID, 'id_first_partner_hiv')
    partner_hiv_test = (By.ID, 'id_partner_hiv_test')
    first_disclose = (By.ID, 'id_first_disclose')
    first_condom_freq = (By.ID, 'id_first_condom_freq')
    first_partner_cp = (By.ID, 'id_first_partner_cp')

    def set_report_date(self, report_date):
        date_element = self.browser.find_element(*RecentPartnerPage.report_date)
        date_element.send_keys(report_date)

    def set_report_time(self, report_time):
        time_element = self.browser.find_element(*RecentPartnerPage.report_time)
        time_element.send_keys(report_time)

    def set_first_partner_live(self, first_partner_live):
        first_partner_live_element = self.browser.find_element(*RecentPartnerPage.first_partner_live)
        first_partner_live_element.send_keys(first_partner_live)

    def set_sex_partner_community(self, sex_partner_community):
        sex_partner_community_element = self.browser.find_element(*RecentPartnerPage.sex_partner_community)
        sex_partner_community_element.send_keys(sex_partner_community)

    def set_past_year_sex_freq(self, past_year_sex_freq):
        past_year_sex_freq_element = self.browser.find_element(*RecentPartnerPage.past_year_sex_freq)
        past_year_sex_freq_element.send_keys(past_year_sex_freq)

    def set_third_last_sex(self, third_last_sex):
        third_last_sex_element = self.browser.find_element(*RecentPartnerPage.third_last_sex)
        third_last_sex_element.send_keys(third_last_sex)

    def set_first_first_sex(self, first_first_sex):
        first_first_sex_element = self.browser.find_element(*RecentPartnerPage.first_first_sex)
        first_first_sex_element.send_keys(first_first_sex)

    def set_first_sex_current(self, first_sex_current):
        first_sex_current_element = self.browser.find_element(*RecentPartnerPage.first_sex_current)
        first_sex_current_element.send_keys(first_sex_current)

    def set_first_relationship(self, first_relationship):
        first_relationship_element = self.browser.find_element(*RecentPartnerPage.first_relationship)
        first_relationship_element.send_keys(first_relationship)

    def set_first_exchange(self, first_exchange):
        first_exchange_element = self.browser.find_element(*RecentPartnerPage.first_exchange)
        first_exchange_element.send_keys(first_exchange)

    def set_concurrent(self, concurrent):
        concurrent_element = self.browser.find_element(*RecentPartnerPage.concurrent)
        concurrent_element.send_keys(concurrent)

    def set_goods_exchange(self, goods_exchange):
        goods_exchange_element = self.browser.find_element(*RecentPartnerPage.goods_exchange)
        goods_exchange_element.send_keys(goods_exchange)

    def set_first_sex_freq(self, first_sex_freq):
        first_sex_freq_element = self.browser.find_element(*RecentPartnerPage.first_sex_freq)
        first_sex_freq_element.send_keys(first_sex_freq)

    def set_first_partner_hiv(self, first_partner_hiv):
        first_partner_hiv_element = self.browser.find_element(*RecentPartnerPage.first_partner_hiv)
        first_partner_hiv_element.send_keys(first_partner_hiv)

    def set_partner_hiv_test(self, partner_hiv_test):
        partner_hiv_test_element = self.browser.find_element(*RecentPartnerPage.partner_hiv_test)
        partner_hiv_test_element.send_keys(partner_hiv_test)

    def set_first_disclose(self, first_disclose):
        first_disclose_element = self.browser.find_element(*RecentPartnerPage.first_disclose)
        first_disclose_element.send_keys(first_disclose)

    def set_first_condom_freq(self, first_condom_freq):
        first_condom_freq_element = self.browser.find_element(*RecentPartnerPage.first_condom_freq)
        first_condom_freq_element.send_keys(first_condom_freq)

    def set_first_partner_cp(self, first_partner_cp):
        first_partner_cp_element = self.browser.find_element(*RecentPartnerPage.first_partner_cp)
        first_partner_cp_element.send_keys(first_partner_cp)

    def fill_recent_partner(self, report_date, report_time, first_partner_live, sex_partner_community,
                            past_year_sex_freq, third_last_sex, first_first_sex, first_sex_current,
                            first_relationship, first_exchange, concurrent, goods_exchange, first_sex_freq,
                            first_partner_hiv, partner_hiv_test, first_disclose, first_condom_freq, first_partner_cp):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.set_first_partner_live(first_partner_live)
        self.set_sex_partner_community(sex_partner_community)
        self.set_past_year_sex_freq(past_year_sex_freq)
        self.set_third_last_sex(third_last_sex)
        self.set_first_first_sex(first_first_sex)
        self.set_first_sex_current(first_sex_current)
        self.set_first_relationship(first_relationship)
        self.set_first_exchange(first_exchange)
        self.set_concurrent(concurrent)
        self.set_goods_exchange(goods_exchange)
        self.set_first_sex_freq(first_sex_freq)
        self.set_first_partner_hiv(first_partner_hiv)
        self.set_partner_hiv_test(partner_hiv_test)
        self.set_first_disclose(first_disclose)
        self.set_first_condom_freq(first_condom_freq)
        self.set_first_partner_cp(first_partner_cp)
        self.save_button()
