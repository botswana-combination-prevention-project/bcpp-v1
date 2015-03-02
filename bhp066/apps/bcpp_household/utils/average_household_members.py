from ..models import HouseholdStructure
from apps.bcpp_household_member.models.household_member import HouseholdMember


def average_household_members():
    number_enumerated = HouseholdMember.objects.all().count()
    number_of_households = HouseholdStructure.objects.filter(enumerated=True).count()
    return None 