import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import CeaEnrolmentChecklist
from bhp_registration.tests.factories import RegisteredSubjectFactory


class CeaEnrolmentChecklistFactory(BaseScheduledModelFactory):
    FACTORY_FOR = CeaEnrolmentChecklist

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    mental_capacity = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    incarceration = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    citizen = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    community_resident = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    enrolment_reason = (('CD4 < 50', 'Most recent (within past 3 months) CD4 < 50'), ('CD4 50-100', 'Most recent (within past 3 months) CD4 50-100'), ('AIDS opportunistic infection/condition', 'Current AIDS opportunistic infection/condition'))[0][0]
    cd4_date = date.today()
    cd4_count = 2.5
    opportunistic_illness = (('Tuberculosis', 'Tuberculosis'), ('Wasting', 'Wasting'), ('Cryptococcosis', 'Cryptococcosis'), ('severe bacterial pneumonia', 'Recurrent severe bacterial pneumonia'), ('Esophageal candidiasis', 'Esophageal candidiasis'), ('Pneumocystis pneumonia', 'Pneumocystis pneumonia'), ("Kaposi's sarcoma", "Kaposi's sarcoma"), ('Cervical cancer', 'Cervical cancer'), ("Non-Hodgkin's lymphoma", "Non-Hodgkin's lymphoma"), ('Other, record', 'Other, record'), ('No current AIDS opportunistic illness', 'No current AIDS opportunistic illness'))[0][0]
    diagnosis_date = date.today()
    date_signed = datetime.today()
