from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from edc.map.classes import Mapper, site_mappers
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc.subject.rule_groups.classes import site_rule_groups

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from ..classes import SubjectStatusHelper

from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (
    SubjectReferralFactory, ReproductiveHealthFactory,
    HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory,
    PimaFactory, HivTestReviewFactory, HivTestingHistoryFactory, TbSymptomsFactory,
    HivResultDocumentationFactory)


class TestPlotMapper(Mapper):
    map_area = 'test_community84'
    map_code = '097'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033182
    gps_center_lon = 25.747179
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class SubjectStatusHelperTests(BaseScheduledModelTestCase):

    community = 'test_community81'

    def tests_(self):