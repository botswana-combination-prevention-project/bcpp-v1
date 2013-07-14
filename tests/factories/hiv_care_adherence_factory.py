import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HivCareAdherence


class HivCareAdherenceFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivCareAdherence

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    medical_care = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    arv_naive = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    why_no_arv_other = factory.Sequence(lambda n: 'why_no_arv_other{0}'.format(n))
    on_arv = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    arv_stop_other = factory.Sequence(lambda n: 'arv_stop_other{0}'.format(n))
