import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Cancer


class CancerFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Cancer

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    date_cancer = date.today()
    dx_cancer = (("Kaposi's sarcoma (KS)", "Kaposi's sarcoma (KS)"), ('Cervical cancer', 'Cervical cancer'), ('Breast cancer', 'Breast cancer'), ("Non-Hodgkin's lymphoma (NHL)", "Non-Hodgkin's lymphoma (NHL)"), ('Colorectal cancer', 'Colorectal cancer'), ('Prostate cancer', 'Prostate cancer'), ('Cancer of mouth, throat, voice box (larynx)', 'Cancer of mouth, throat, voice box (larynx)'), ('Cancer of oesophagus', 'Cancer of oesophagus'), ('Other', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
