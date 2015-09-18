from datetime import date
from django.test import TestCase
from django.db.models import Model

from bhp066.apps.bcpp_household.models import Plot


class TestPLotSimple(TestCase):

    def test_create(self):

        Plot.save = Model.save

        plot = Plot.objects.create()
        self.assertEqual(plot.created.date(), date.today())
        self.assertEqual(plot.modified.date(), date.today())
        self.assertEqual(plot.user_created, '')
        self.assertEqual(plot.user_modified, '')
        self.assertNotEqual(plot.revision, '')
        self.assertIsNotNone(plot.revision)
        self.assertNotEqual(plot.hostname_created, '')
        self.assertIsNotNone(plot.hostname_created)
