import factory

from ...models import HouseholdMember
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc_constants.constants import MALE, YES, NOT_APPLICABLE


class HouseholdMemberFactory(factory.DjangoModelFactory):

    class Meta:
        model = HouseholdMember

    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    initials = factory.Sequence(lambda n: 'initials{0}'.format(n))
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    gender = MALE
    age_in_years = 25
    present_today = YES
    study_resident = YES
    target = 20
    inability_to_participate = NOT_APPLICABLE
