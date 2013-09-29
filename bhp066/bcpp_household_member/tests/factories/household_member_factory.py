import factory
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.tests.factories import HouseholdStructureFactory
from ...models import HouseholdMember


class HouseholdMemberFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdMember

    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    initials = factory.Sequence(lambda n: 'initials{0}'.format(n))
    gender = (('M', 'Male'), ('F', 'Female'))[0][0]
    age_in_years = 2
    present = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    lives_in_household = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    is_eligible_member = True
    target = 2
    household_structure = factory.SubFactory(HouseholdStructureFactory)
    nights_out = 2
