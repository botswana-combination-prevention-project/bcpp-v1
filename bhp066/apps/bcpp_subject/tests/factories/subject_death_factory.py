import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp_subject.models import SubjectDeath
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.subject.adverse_event.tests.factories import DeathCauseInfoFactory
from edc.subject.adverse_event.tests.factories import DeathCauseCategoryFactory


class SubjectDeathFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectDeath

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    death_date = date.today()
    death_cause_info = factory.SubFactory(DeathCauseInfoFactory)
    death_cause_category = factory.SubFactory(DeathCauseCategoryFactory)
    participant_hospitalized = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    days_hospitalized = 2
    sufficient_records = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    document_hiv = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    document_community = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    death_year = date.today()
    decendent_death_age = 2
    hospital_death = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    decedent_haart = (('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure'))[0][0]
    decedent_hospitalized = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    hospital_visits = 2
