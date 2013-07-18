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
    grant_type = (('Child support ', 'Child support '), ('Old age pension', 'Old age pension'), ('Foster care', 'Foster care'), ('Disability', 'Disability (disability dependency)'), ('OTHER', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other_grant = factory.Sequence(lambda n: 'other_grant{0}'.format(n))
