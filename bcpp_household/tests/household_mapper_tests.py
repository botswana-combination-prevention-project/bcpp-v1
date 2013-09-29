from django.test import TestCase
from ..mappers import MochudiHouseholdMapper
from ..models import Plot


class HouseholdMapperTests(TestCase):

    def test_p1(self):

        mapper = MochudiHouseholdMapper()

        self.assertEqual(mapper.item_model, Plot)
        print 'assert instance attribute is set by class attribute.'
        self.assertEqual(mapper.get_item_model_cls(), Plot)
