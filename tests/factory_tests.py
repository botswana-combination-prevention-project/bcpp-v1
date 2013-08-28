from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from bhp_content_type_map.models import ContentTypeMap
from factories import VisitDefinitionFactory, ScheduleGroupFactory, MembershipFormFactory
from bhp_visit.models import MembershipForm, ScheduleGroup, VisitDefinition
from bhp_content_type_map.classes import ContentTypeMapHelper


class FactoryTests(TestCase):

    def test_p1(self):
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type = ContentType.objects.get(app_label='bhp_base_test', model='testconsentwithmixin')
        self.assertIsInstance(content_type, ContentType)
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        self.assertIsInstance(content_type_map, ContentTypeMap)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        self.assertIsInstance(membership_form, MembershipForm)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form)
        self.assertIsInstance(schedule_group, ScheduleGroup)
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')
        visit_definition = VisitDefinitionFactory(visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        self.assertIsInstance(visit_definition, VisitDefinition)
        self.assertEqual(visit_definition.schedule_group.all().count(), 1)
