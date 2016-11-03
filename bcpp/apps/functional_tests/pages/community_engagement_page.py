from selenium.webdriver.common.by import By
from .base_page import BaseModelAdminPage


class CommunityEngagementPage(BaseModelAdminPage):
    report_date = (By.ID, 'id_report_datetime_0')
    report_time = (By.ID, 'id_report_datetime_1')
    community_engagement = (By.ID, 'id_community_engagement')
    vote_engagement = (By.ID, 'id_vote_engagement')
    problems_engagement = (By.ID, 'id_problems_engagement')
    solve_engagement = (By.ID, 'id_solve_engagement')

    def set_report_date(self, date):
        date_element = self.browser.find_element(*CommunityEngagementPage.report_date)
        date_element.send_keys(date)

    def set_report_time(self, time):
        date_element = self.browser.find_element(*CommunityEngagementPage.report_time)
        date_element.send_keys(time)

    def set_community_engagement(self, community_engagement):
        date_element = self.browser.find_element(*CommunityEngagementPage.community_engagement)
        date_element.send_keys(community_engagement)

    def set_vote_engagement(self, vote_engagement):
        date_element = self.browser.find_element(*CommunityEngagementPage.vote_engagement)
        date_element.send_keys(vote_engagement)

    def set_solve_engagement(self, solve_engagement):
        date_element = self.browser.find_element(*CommunityEngagementPage.solve_engagement)
        date_element.send_keys(solve_engagement)

    def fill_community_engagement(self, report_date, report_time, community_engagement, vote_engagement,
                                  problems_engagement, solve_engagement):
        self.set_report_date(report_date)
        self.set_report_time(report_time)
        self.community_engagement(community_engagement)
        self.vote_engagement(vote_engagement)
        self.problems_engagement(solve_engagement)
        self.save_button()
