import factory
from datetime import date, datetime
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import CeaEnrollmentChecklist


class CeaEnrollmentChecklistFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CeaEnrollmentChecklist

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    citizen = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    community_resident = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8890>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b88d0>'), ('REF', '<django.utils.functional.__proxy__ object at 0x1021b8910>'))[0][0]
    enrollment_reason = (('CD4 < 50', u'Most recent (within past 3 months) CD4 < 50'), ('CD4 50-100', u'Most recent (within past 3 months) CD4 50-100'), ('AIDS opportunistic infection/condition', u'Current AIDS opportunistic infection/condition'))[0][0]
    cd4_date = date.today()
    cd4_count = 2.5
    opportunistic_illness = (('Tuberculosis', u'Tuberculosis'), ('Wasting', u'Wasting'), ('Cryptococcosis', u'Cryptococcosis'), ('severe bacterial pneumonia', u'Recurrent severe bacterial pneumonia'), ('Esophageal candidiasis', u'Esophageal candidiasis'), ('Pneumocystis pneumonia', u'Pneumocystis pneumonia'), ("Kaposi's sarcoma", u"Kaposi's sarcoma"), ('Cervical cancer', u'Cervical cancer'), ("Non-Hodgkin's lymphoma", u"Non-Hodgkin's lymphoma"), ('Other, record', u'Other, record'), ('No current AIDS opportunistic illness', u'No current AIDS opportunistic illness'))[0][0]
    diagnosis_date = date.today()
    date_signed = datetime.today()
