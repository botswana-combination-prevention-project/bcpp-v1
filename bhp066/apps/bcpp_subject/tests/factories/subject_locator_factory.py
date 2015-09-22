import factory

from datetime import date, datetime

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from .subject_visit_factory import SubjectVisitFactory

from ...models import SubjectLocator


class SubjectLocatorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubjectLocator

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = datetime.today()
    date_signed = date.today()
    home_visit_permission = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    subject_cell = '72777777'
    may_follow_up = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    may_call_work = (('Yes', 'Yes'), ('No', 'No'), ('Doesnt_work', 'Doesnt Work'))[0][0]
    may_contact_someone = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    has_alt_contact = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
