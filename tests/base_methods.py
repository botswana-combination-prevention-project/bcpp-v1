from datetime import datetime
from bhp_variables.models import StudySite, StudySpecific
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_content_type_map.models import ContentTypeMap
from bhp_consent.models import ConsentCatalogue, TestSubjectConsent


class BaseMethods(object):

    def create_study_variables(self):
        self.study_site = StudySite.objects.create(site_code='10', site_name='TEST_SITE')
        self.study_specific = StudySpecific.objects.create(
            protocol_number='TEST',
            protocol_code='TEST',
            protocol_title='TEST TITLE',
            research_title='TEST RESEARCH TITLE',
            minimum_age_of_consent=16,
            maximum_age_of_consent=99,
            age_at_adult_lower_bound=18,
            gender_of_consent='MF',
            subject_identifier_prefix='000',
            study_start_datetime=datetime(datetime.today().year - 1, 1, 1),
            device_id=0)

    def prepare_consent_catalogue(self):
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        # prepare the consent catalogue
        content_type_map = ContentTypeMap.objects.get(model__iexact=TestSubjectConsent._meta.object_name)
        ConsentCatalogue.objects.create(
            name='consent',
            content_type_map=content_type_map,
            consent_type='study',
            version=1,
            start_datetime=StudySpecific.objects.all()[0].study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app='bhp_consent')

    def create_consent(self):
        subject_consent = TestSubjectConsent.objects.create(
            first_name='TEST',
            last_name='TESTER',
            user_provided_subject_identifier=None,
            initials='TT',
            identity='111111111',
            confirm_identity='111111111',
            identity_type='omang',
            dob=datetime(1990, 01, 01),
            is_dob_estimated='No',
            gender='M',
            subject_type='subject',
            consent_datetime=datetime.today(),
            study_site=self.study_site,
            may_store_samples='Yes')
        return subject_consent