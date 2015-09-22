import factory

from ...models import HouseholdMember


class HouseholdMemberFactory(factory.DjangoModelFactory):

    class Meta:
        model = HouseholdMember

    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    initials = factory.Sequence(lambda n: 'initials{0}'.format(n))
    gender = (('M', 'Male'), ('F', 'Female'))[0][0]
    age_in_years = 25
    present_today = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    study_resident = 'Yes'
    target = 20
    inability_to_participate = 'N/A'
    
