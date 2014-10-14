import factory
from datetime import datetime, date
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import ClinicEligibility


class ClinicEligibilityFactory(BaseUuidModelFactory):
    FACTORY_FOR = ClinicEligibility

    registration_datetime = datetime.today()
    #registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    first_name = factory.Sequence(lambda n: 'name{0}'.format(n))
    dob = date(date.today().year - 20, 1, 1)
    gender = 'M'
    initials = factory.Sequence(lambda n: 'M{0}'.format(n))
    part_time_resident = (('Yes', 'Yes'), ('No', 'No'), ('DWTA', 'Don\'t want to answer'))[0][0]
    hiv_status = (('POS', 'HIV Positive'), ('NEG', 'HIV Negative'), ('IND', 'Indeterminate'), ('UNK', 'I am not sure'), ('not_answering', 'Don\'t want to answer'))[0][0]
    legal_marriage = 'Yes'
    inability_to_participate = 'None'
