import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SubjectDeath
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_adverse.tests.factories import DeathCauseInfoFactory
from bhp_adverse.tests.factories import DeathCauseCategoryFactory


class SubjectDeathFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SubjectDeath

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    death_date = date.today()
    death_cause_info = factory.SubFactory(DeathCauseInfoFactory)
    death_cause_category = factory.SubFactory(DeathCauseCategoryFactory)
    participant_hospitalized = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    days_hospitalized = 1
    sufficient_records = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    document_hiv = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    document_community = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    death_year = date.today()
    decendent_death_age = 1
    hospital_death = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    decedent_haart = (('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure'))[0][0]
    decedent_hospitalized = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    hospital_visits = 1
