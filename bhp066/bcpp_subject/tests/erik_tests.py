from django import forms
from django.test import TestCase
from bcpp_subject.forms import AccessToCareForm
from datetime import datetime
from bhp_lab_tracker.classes import lab_tracker
from bhp_appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from bhp_content_type_map.models import ContentTypeMap
from bhp_content_type_map.classes import ContentTypeMapHelper
from bcpp_subject.models import SubjectConsent


class ErikTests(TestCase):

    app_label = 'bcpp_subject'

    def test_p1(self):
        lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()

        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(model__iexact=SubjectConsent._meta.object_name)
        ConsentCatalogueFactory(
            name=self.app_label,
            content_type_map=content_type_map,
            consent_type='study',
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)

        # AccessToCareForm
        frm = AccessToCareForm()
        frm.cleaned_data = {'access_care': 'OTHER', 'access_care_other': ''}
        self.assertRaises(forms.ValidationError, frm.clean)