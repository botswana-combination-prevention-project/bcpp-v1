from datetime import datetime, date, timedelta

from django.test import SimpleTestCase

from edc.map.classes import Mapper, site_mappers
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc.subject.rule_groups.classes import site_rule_groups

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from ..classes import SubjectStatusHelper


class TestPlotMapper(Mapper):
    map_area = 'test_community82'
    map_code = '097'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033192
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class TestSubjectReferralApptHelper(SimpleTestCase):

    community = 'test_community82'

    def test_idcc(self):
        """Assert POS! referred to IDCC on next day if not pregnant"""
        referral_code = 'POS!-LO'
