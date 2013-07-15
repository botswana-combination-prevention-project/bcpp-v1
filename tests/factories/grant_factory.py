import factory
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Grant
from bcpp_subject.tests.factories import LabourMarketWagesFactory


class GrantFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Grant

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    labour_market_wages = factory.SubFactory(LabourMarketWagesFactory)
    grant_number = 1
    grant_type = (('Child support ', 'Child support '), ('Old age pension', 'Old age pension'), ('Foster care', 'Foster care'), ('Disability', 'Disability (disability dependency)'), ('OTHER', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other_grant = factory.Sequence(lambda n: 'other_grant{0}'.format(n))
