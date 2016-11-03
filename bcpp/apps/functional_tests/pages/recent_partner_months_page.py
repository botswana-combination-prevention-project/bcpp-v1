from .detailed_sexual_history_page import DetailedSexualHistoryPage


class RecentPartnerPage(DetailedSexualHistoryPage):

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
