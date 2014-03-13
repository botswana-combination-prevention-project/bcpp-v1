import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp_household.tests.factories import HouseholdStructureFactory
from ...models import HouseholdMember


class HouseholdMemberFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdMember

    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    initials = factory.Sequence(lambda n: 'initials{0}'.format(n))
    gender = (('M', 'Male'), ('F', 'Female'))[0][0]
    age_in_years = 2
    present_today = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    target = 20
    household_structure = factory.SubFactory(HouseholdStructureFactory)
    eligible_subject = True
    eligible_member = True