from datetime import datetime

from django.core.management import call_command
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory

from edc.map.classes import Mapper, site_mappers
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.entry.models import Entry
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_schedule.models import VisitDefinition, MembershipForm, ScheduleGroup
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory

from apps.bcpp_household.models import Plot, Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_survey.tests.factories import SurveyFactory

from .factories import SubjectConsentFactory, SubjectVisitFactory
from ..visit_schedule import conf


class TestPlotMapper(Mapper):
    map_area = 'test_community9'
    map_code = '097'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033162
    gps_center_lon = 25.747149
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class RuleGroupTests(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community9'

    def setUp(self):

        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()

        content_type_map = ContentTypeMap.objects.get(content_type__model='SubjectConsent'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)

        for category, definition in conf.membership_forms.iteritems():
            if not MembershipForm.objects.filter(category=category):
                MembershipForm.objects.create(
                    category=category,
                    app_label=definition[1]._meta.app_label,
                    model_name=definition[1]._meta.object_name,
                    content_type_map=ContentTypeMap.objects.get(app_label=definition[1]._meta.app_label, module_name=definition[1]._meta.object_name.lower()),
                    visible=definition[2])
        for group_name, definition in conf.schedule_groups.iteritems():
            if not ScheduleGroup.objects.filter(group_name=group_name):
                ScheduleGroup.objects.create(
                    group_name=group_name,
                    membership_form=MembershipForm.objects.get(category=definition[1]),
                    grouping_key=definition[2],
                    comment=definition[3])
        for code, definition in conf.visit_definitions.iteritems():
            if not VisitDefinition.objects.filter(code=code):
                visit_tracking_content_type_map = ContentTypeMap.objects.get(app_label=definition.get('visit_tracking_model')._meta.app_label, module_name=definition.get('visit_tracking_model')._meta.object_name.lower())
                schedule_group = ScheduleGroup.objects.get(group_name=definition.get('schedule_group'))
                visit_definition = VisitDefinition.objects.create(
                    code=code,
                    title=definition.get('title'),
                    time_point=definition.get('time_point'),
                    base_interval=definition.get('base_interval'),
                    base_interval_unit=definition.get('base_interval_unit'),
                    lower_window=definition.get('window_lower_bound'),
                    lower_window_unit=definition.get('window_lower_bound_unit'),
                    upper_window=definition.get('window_upper_bound'),
                    upper_window_unit=definition.get('window_upper_bound_unit'),
                    grouping=definition.get('grouping'),
                    visit_tracking_content_type_map=visit_tracking_content_type_map,
                    instruction=definition.get('instructions') or '-',
                    )
                visit_definition.schedule_group.add(schedule_group)
                for entry in definition.get('entries'):
                    if not Entry.objects.filter(app_label=entry[1], model_name=entry[2]):
                        content_type_map = ContentTypeMap.objects.get(app_label=entry[1], module_name=entry[2].lower())
                        Entry.objects.create(
                            content_type_map=content_type_map,
                            visit_definition=visit_definition,
                            entry_order=entry[0],
                            app_label=entry[1],
                            model_name=entry[2])

        self.survey = SurveyFactory()

        plot = PlotFactory(community=self.community, household_count=1, status='occupied')

        household_structure = HouseholdStructure.objects.get(household__plot=plot)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)

        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure, gender='F')
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure, gender='M')
        self.household_member_female.eligible_member = True
        self.household_member_male.eligible_member = True
        self.household_member_female.eligible_subject = True
        self.household_member_male.eligible_subject = True
        self.household_member_female.save()
        self.household_member_male.save()

        subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female, gender='F')
        subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male, gender='M')

        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female)
        self.subject_visit_female = SubjectVisitFactory(appointment=appointment_female, household_member=self.household_member_female)
        appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male)
        self.subject_visit_male = SubjectVisitFactory(appointment=appointment_male, household_member=self.household_member_male)

    def test_p1(self):
        pass
