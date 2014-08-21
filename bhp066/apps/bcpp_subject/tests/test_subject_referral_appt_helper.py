from datetime import datetime, date, timedelta

from django.db import transaction

from edc.map.classes import Mapper, site_mappers
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc.subject.rule_groups.classes import site_rule_groups

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from ..classes import SubjectStatusHelper

from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (
    HivCareAdherenceFactory, HivResultFactory,
    HivTestReviewFactory, HivTestingHistoryFactory,
    HivResultDocumentationFactory)


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


class TestSubjectReferralApptHelper(BaseScheduledModelTestCase):

    community = 'test_community82'

    def tests_hiv_result(self):
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)
