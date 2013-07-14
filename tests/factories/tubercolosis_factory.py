import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Tubercolosis


class TubercolosisFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Tubercolosis

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    date_tb = date.today()
    dx_tb = (('Pulmonary tuberculosis', 'Pulmonary tuberculosis'), ('Extrapulmonary (outside the lungs) tuberculosis', 'Extrapulmonary (outside the lungs) tuberculosis'), ('Other', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
