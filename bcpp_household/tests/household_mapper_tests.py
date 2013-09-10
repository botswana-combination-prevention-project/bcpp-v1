from django.test import TestCase
from bcpp_household.mappers import MochudiHouseholdMapper
from bcpp_household.models import Household


class HouseholdMapperTests(TestCase):

    def test_p1(self):

        mapper = MochudiHouseholdMapper()

        self.assertEqual(mapper.item_model, Household)
        print 'assert instance attribute is set by class attribute.'
        self.assertEqual(mapper.get_item_model_cls(), Household)
