import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import CeaEnrolmentChecklist
from bhp_registration.tests.factories import RegisteredSubjectFactory


class CeaEnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = CeaEnrolmentChecklist

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    mental_capacity = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48e50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48ed0>))[0][0]
    incarceration = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48e50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48ed0>))[0][0]
    citizen = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48e50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48ed0>))[0][0]
    community_resident = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    enrolment_reason = (('CD4 < 50', u'Most recent (within past 3 months) CD4 < 50'), ('CD4 50-100', u'Most recent (within past 3 months) CD4 50-100'), ('AIDS opportunistic infection/condition', u'Current AIDS opportunistic infection/condition'))[0][0]
    cd4_date = date.today()
    cd4_count = 2.5
    opportunistic_illness = (('Tuberculosis', u'Tuberculosis'), ('Wasting', u'Wasting'), ('Cryptococcosis', u'Cryptococcosis'), ('severe bacterial pneumonia', u'Recurrent severe bacterial pneumonia'), ('Esophageal candidiasis', u'Esophageal candidiasis'), ('Pneumocystis pneumonia', u'Pneumocystis pneumonia'), ("Kaposi's sarcoma", u"Kaposi's sarcoma"), ('Cervical cancer', u'Cervical cancer'), ("Non-Hodgkin's lymphoma", u"Non-Hodgkin's lymphoma"), ('Other, record', u'Other, record'), ('No current AIDS opportunistic illness', u'No current AIDS opportunistic illness'))[0][0]
    diagnosis_date = date.today()
    date_signed = datetime.today()
