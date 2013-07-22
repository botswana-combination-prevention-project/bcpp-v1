import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import CommunityEngagement


class CommunityEngagementFactory(BaseUuidModelFactory):
    FACTORY_FOR = CommunityEngagement

    report_datetime = datetime.today()
    community_engagement = (('Very active', <django.utils.functional.__proxy__ object at 0x103ae5d50>), ('Somewhat active', <django.utils.functional.__proxy__ object at 0x103ae5dd0>), ('Not active at all', <django.utils.functional.__proxy__ object at 0x103ae5e50>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae5ed0>))[0][0]
    vote_engagement = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae5f50>), ('No', <django.utils.functional.__proxy__ object at 0x103ae5fd0>), ("Not applicable (no election, can't vote)", <django.utils.functional.__proxy__ object at 0x103ae7090>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae7110>))[0][0]
    problems_engagement_other = factory.Sequence(lambda n: 'problems_engagement_other{0}'.format(n))
    solve_engagement = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae7190>), ('No', <django.utils.functional.__proxy__ object at 0x103ae7210>), ("Don't know", <django.utils.functional.__proxy__ object at 0x103ae7290>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae7310>), ('None', <django.utils.functional.__proxy__ object at 0x103ae7390>))[0][0]
