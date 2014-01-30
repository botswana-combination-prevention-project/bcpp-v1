from .household_member_report_query import HouseholdMemberReportQuery
from .report_query import TwoColumnReportQuery


class IndicatorsReportQuery(TwoColumnReportQuery):

    def post_init(self, **kwargs):
        self.member_query = HouseholdMemberReportQuery(self.community, self.start_date, self.end_date)

    def display_title(self):
        pass

    def data_to_display(self):
        pass

    def eligible_participants_count(self):
        return self.member_query.study_eligible_qs().count()

    def participants_percentage(self):
        return self.eligible_participants_count() * 100.0 / self._potential_participants_count()

    def _potential_participants_count(self):
        return self.member_query.age_eligible_qs().count() or 1

    def positive_participants_count(self):
        return self.member_query.hiv_positive_qs().count()

    def positive_percentage(self):
        return self.positive_participants_count() * 100.0 / self._potential_participants_count()
