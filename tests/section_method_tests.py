from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from bhp_section.classes.base_section_index_view import BaseSectionIndexView
from bhp_section.classes import site_sections, BaseSectionView


class SectionOneView(BaseSectionView):
    section_name = 'one'
    section_display_name = 'Thing One'
    section_display_index = 110
site_sections.register(SectionOneView)


class SectionTwoView(BaseSectionView):
    section_name = 'two'
    section_display_name = 'Thing Two'
    section_display_index = 110
site_sections.register(SectionTwoView)


class SectionThreeView(BaseSectionView):
    section_name = 'three'
    section_display_name = 'Thing Three'
    section_display_index = 100


class SectionMethodTests(TestCase):

    def test_controller(self):

        self.assertEqual(site_sections.get_section_names(), ['one', 'two'])
        self.assertEqual(site_sections.get_section_display_names(), ['Thing One', 'Thing Two'])
        self.assertEqual(site_sections.get_section_list(), site_sections.get_section_tuples())
        self.assertEqual(sorted([tpl.section_name for tpl in site_sections.get_section_tuples()]), sorted(site_sections.get_section_names()))
        self.assertEqual(sorted([tpl.display_name for tpl in site_sections.get_section_tuples()]), sorted(site_sections.get_section_display_names()))
        self.assertRaises(ImproperlyConfigured, site_sections.get_section_display_indexes)
        site_sections.unregister('two')
        site_sections.register(SectionThreeView)
        self.assertEqual(site_sections.get_section_display_indexes(), [100, 110])
        self.assertEqual(site_sections.get_section_names(), ['one', 'three'])
        self.assertEqual(site_sections.get_section_display_names(), ['Thing One', 'Thing Three'])
        self.assertEqual(site_sections.get_indexed_section_display_names(), ['Thing Three', 'Thing One'])
        self.assertEqual(site_sections.get_section_list(), site_sections.get_section_tuples())
        self.assertEqual(sorted([tpl.section_name for tpl in site_sections.get_section_tuples()]), sorted(site_sections.get_section_names()))
        self.assertEqual(sorted([tpl.display_name for tpl in site_sections.get_section_tuples()]), sorted(site_sections.get_section_display_names()))

        site_sections.autodiscover()
        self.assertTrue(site_sections.is_autodiscovered)

        section_index_view = BaseSectionIndexView()
        self.assertEqual(section_index_view.get_section_display_name_list(), ['Thing One', 'Thing Three'])
        self.assertEqual(section_index_view.get_indexed_section_display_name_list(), ['Thing Three', 'Thing One'])
        self.assertFalse(section_index_view.is_setup)
        section_index_view.setup()
        self.assertTrue(section_index_view.is_setup)
