from bhp_registration.models import BaseRegistrationModel
from bhp_base_test.managers import TestRegistrationManager
from test_off_study_mixin import TestOffStudyMixin
from test_base_off_study import TestBaseOffStudy


class TestRegistration(TestOffStudyMixin, BaseRegistrationModel):

    objects = TestRegistrationManager()

    def get_off_study_cls(self):
        return TestBaseOffStudy

    class Meta:
        app_label = 'bhp_base_test'
