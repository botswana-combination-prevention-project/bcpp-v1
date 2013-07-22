import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import CeaEnrolmentChecklist
from bhp_registration.tests.factories import RegisteredSubjectFactory


class CeaEnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = CeaEnrolmentChecklist

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    mental_capacity = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    incarceration = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    citizen = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    community_resident = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    enrolment_reason = (('CD4 < 50', <django.utils.functional.__proxy__ object at 0x103a23350>), ('CD4 50-100', <django.utils.functional.__proxy__ object at 0x103a233d0>), ('AIDS opportunistic infection/condition', <django.utils.functional.__proxy__ object at 0x103a23450>))[0][0]
    cd4_date = date.today()
    cd4_count = 2.5
    opportunistic_illness = (('Tuberculosis', <django.utils.functional.__proxy__ object at 0x103a234d0>), ('Wasting', <django.utils.functional.__proxy__ object at 0x103a23550>), ('Cryptococcosis', <django.utils.functional.__proxy__ object at 0x103a235d0>), ('severe bacterial pneumonia', <django.utils.functional.__proxy__ object at 0x103a23650>), ('Esophageal candidiasis', <django.utils.functional.__proxy__ object at 0x103a236d0>), ('Pneumocystis pneumonia', <django.utils.functional.__proxy__ object at 0x103a23750>), ("Kaposi's sarcoma", <django.utils.functional.__proxy__ object at 0x103a237d0>), ('Cervical cancer', <django.utils.functional.__proxy__ object at 0x103a23850>), ("Non-Hodgkin's lymphoma", <django.utils.functional.__proxy__ object at 0x103a238d0>), ('Other, record', <django.utils.functional.__proxy__ object at 0x103a23950>), ('No current AIDS opportunistic illness', <django.utils.functional.__proxy__ object at 0x103a239d0>))[0][0]
    diagnosis_date = date.today()
    date_signed = datetime.today()
