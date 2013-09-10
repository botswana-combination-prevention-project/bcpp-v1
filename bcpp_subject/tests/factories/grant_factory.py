import factory
from bcpp_subject.models import Grant
from bcpp_subject.tests.factories import LabourMarketWagesFactory
from bcpp_subject.tests.factories import BaseScheduledInlineModelFactory


class GrantFactory(BaseScheduledInlineModelFactory):
    FACTORY_FOR = Grant

    #report_datetime = datetime.today()
    labour_market_wages = factory.SubFactory(LabourMarketWagesFactory)
    grant_number = 2
    grant_type = (('Child support ', u'Child support '), ('Old age pension', u'Old age pension'), ('Foster care', u'Foster care'), ('Disability', u'Disability (disability dependency)'), ('OTHER', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    other_grant = factory.Sequence(lambda n: 'other_grant{0}'.format(n))
