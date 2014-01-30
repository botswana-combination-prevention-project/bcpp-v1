import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import ClinicEligibility


class ClinicEligibilityFactory(BaseUuidModelFactory):
    FACTORY_FOR = ClinicEligibility
    
    registration_datetime = datetime.today()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    part_time_resident = (('Yes', 'Yes'), ('No', 'No'), ('DWTA', 'Don\'t want to answer'))[0][0]
    hiv_status = ('POS', 'HIV Positive'), ('NEG', 'HIV Negative'), ('IND', 'Indeterminate'), ('UNK', 'I am not sure'), ('not_answering', 'Don\'t want to answer')[0][0]
