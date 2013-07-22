import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Grant
from bcpp_subject.tests.factories import LabourMarketWagesFactory


class GrantFactory(BaseUuidModelFactory):
    FACTORY_FOR = Grant

    report_datetime = datetime.today()
    labour_market_wages = factory.SubFactory(LabourMarketWagesFactory)
    grant_number = 2
    grant_type = (('Child support ', <django.utils.functional.__proxy__ object at 0x103a20b50>), ('Old age pension', <django.utils.functional.__proxy__ object at 0x103a20bd0>), ('Foster care', <django.utils.functional.__proxy__ object at 0x103a20c50>), ('Disability', <django.utils.functional.__proxy__ object at 0x103a20cd0>), ('OTHER', <django.utils.functional.__proxy__ object at 0x103a20d50>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a20dd0>))[0][0]
    other_grant = factory.Sequence(lambda n: 'other_grant{0}'.format(n))
