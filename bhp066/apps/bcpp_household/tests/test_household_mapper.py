from django.test import TestCase

from ..mappers import BasePlotMapper

from bhp066.apps.bcpp_household.models import Plot


class OtsePlotMapper(BasePlotMapper):
    map_area = 'test_community'
    map_code = '01'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()


class TestHouseholdMapper(TestCase):

    def test_p1(self):
        mapper = OtsePlotMapper()
        self.assertEqual(mapper.item_model_cls, Plot)
        self.assertEqual(mapper.item_model, Plot)
