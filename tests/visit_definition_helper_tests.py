from django.test import TestCase
from bhp_entry.tests.factories import EntryFactory
from bhp_visit.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_content_type_map.models import ContentTypeMap
from bhp_visit_tracking.models import TestSubjectVisit, TestSubjectVisitTwo, TestSubjectVisitThree
from bhp_consent.models import TestSubjectUuidModel
from bhp_visit.classes import VisitDefinitionHelper
from bhp_visit.models import VisitDefinition
from bhp_entry.models import Entry


class VisitDefinitionHelperTests(TestCase):

    def test_copy(self):

        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

        print 'setup a visit definition'
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestSubjectUuidModel._meta.object_name.lower())
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='Group Name', grouping_key='Grouping Key')
        visit_definition = VisitDefinitionFactory(code='1000', title='visit 1000', grouping='Grouping', time_point=0, base_interval=0, base_interval_unit='D')
        visit_definition.schedule_group.add(schedule_group)

        print '    add entries'
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestSubjectVisit._meta.object_name.lower())
        entry = EntryFactory(visit_definition=visit_definition, content_type_map=content_type_map)
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestSubjectVisitTwo._meta.object_name.lower())
        entry = EntryFactory(visit_definition=visit_definition, content_type_map=content_type_map)
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestSubjectVisitThree._meta.object_name.lower())
        entry = EntryFactory(visit_definition=visit_definition, content_type_map=content_type_map)

        print 'copy'
        source_visit_definition = VisitDefinition.objects.get(code='1000')
        visit_definition_helper = VisitDefinitionHelper()
        visit_definition_helper.copy(source_visit_definition, code='1010', title='visit 1010', time_point=10, base_interval=1, base_interval_unit='M')

        print 'assert new visit definition exists'
        self.assertEquals(VisitDefinition.objects.filter(code='1010').count(), 1)
        new_visit_definition = VisitDefinition.objects.get(code='1010')
        print 'assert has same schedule group(s)'
        self.assertEqual(source_visit_definition.schedule_group.all().count(), new_visit_definition.schedule_group.all().count())
        print 'assert all entries added'
        self.assertEqual(Entry.objects.filter(visit_definition=source_visit_definition).count(), Entry.objects.filter(visit_definition=new_visit_definition).count())
        for entry in Entry.objects.filter(visit_definition=new_visit_definition):
            print entry