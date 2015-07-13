from django.test import TestCase

from apps.bcpp_subject.tests.factories import PimaVlFactory

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import Mapper, site_mappers
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite

from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from apps.bcpp_tracking.models import SiteTracker
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_household_member.classes  import EnumerationHelper
from apps.bcpp_survey.models import Survey
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from apps.bcpp_lab.models import Panel, AliquotType

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_tracking.classes import TrackerHelper
from apps.bcpp_tracking.models import Tracker, SiteTracker

from apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory


class TestTracker(TestCase):

    app_label = 'bcpp_tracking'
    community = 'rakops'

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        survey = Survey.objects.all().order_by('datetime_start')[0]
        self.study_site = StudySite.objects.get(site_code='33')

        household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure)
        SubjectConsentFactory(
            consent_datetime=datetime.today() + relativedelta(years=-1),
            household_member=self.household_member_male,
            gender='M',
#             dob=self.household_member_male.age_in_years,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            initials=self.household_member_male.initials,
            study_site=self.study_site)
        self.appointment_male = Appointment.objects.get(registered_subject=self.household_member_male.registered_subject,
                        visit_definition__time_point=0)

        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male,
                        household_member=self.household_member_male)

#     def test_tracker(self):
#         """ """
#         PimaVLFactory(
#             pima_type='mobile setting',
#             subject_visit=self.subject_visit_male,
#             site_name='rakops',
#             )
#         self.assertEqual(1, SiteTracker.objects.filter(site_name='rakops').count())

    def test_central_community_tracker(self):

        PimaVlFactory(
            pima_type='mobile setting',
            subject_visit=self.subject_visit_male,
            site_name='rakops',
            )

        tracker = TrackerHelper()
        tracker.update_central_tracker()
#         tracker.update_site_tracker()
        self.assertEqual(1, SiteTracker.objects.filter(site_name='rakops').count())
        self.assertEqual(1, Tracker.objects.all().count())

#     def test_update_producer_tracker(self):
#         pass
