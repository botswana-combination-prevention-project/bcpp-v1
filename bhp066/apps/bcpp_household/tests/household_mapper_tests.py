from django.test import TestCase

from edc.map.classes import Mapper

from bhp066.apps.bcpp_household.models import Plot


class OtsePlotMapper(Mapper):
    map_area = 'otse'
    map_code = '020'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()


class HouseholdMapperTests(TestCase):

    def test_p1(self):
        mapper = OtsePlotMapper()
        self.assertEqual(mapper.item_model, Plot)
        print 'assert instance attribute is set by class attribute.'
        self.assertEqual(mapper.get_item_model_cls(), Plot)
