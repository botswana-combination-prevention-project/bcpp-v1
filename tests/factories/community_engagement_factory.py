import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import CommunityEngagement


class CommunityEngagementFactory(BaseUuidModelFactory):
    FACTORY_FOR = CommunityEngagement

    report_datetime = datetime.today()
    community_engagement = (('Very active', 'Very active'), ('Somewhat active', 'Somewhat active'), ('Not active at all', 'Not active at all'), ("Don't want to answer", "Don't want to answer"))[0][0]
    vote_engagement = (('Yes', 'Yes'), ('No', 'No'), ("Not applicable (no election, can't vote)", "Not applicable (no election, can't vote)"), ("Don't want to answer", "Don't want to answer"))[0][0]
    problems_engagement_other = factory.Sequence(lambda n: 'problems_engagement_other{0}'.format(n))
    solve_engagement = (('Yes', 'Yes'), ('No', 'No'), ("Don't know", "Don't know"), ("Don't want to answer", "Don't want to answer"), ('None', 'No problems'))[0][0]
