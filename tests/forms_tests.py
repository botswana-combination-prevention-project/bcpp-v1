from django.test import TestCase
from bhp_registration.models import RegisteredSubject
from bhp_base_test.forms import TestSubjectUuidModelForm
from base_methods import BaseMethods
from bhp_base_model.tests.factories import TestManyToManyFactory, TestForeignKeyFactory


class FormsTests(TestCase, BaseMethods):

    def test_base_consented_model_form(self):
        from bhp_base_test.tests.factories import TestConsentFactory
        subject_consent = TestConsentFactory()
        self.prepare_consent_catalogue()
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        test_m2m = TestManyToManyFactory(name='test_m2m', short_name='test_m2m')
        test_fk = TestForeignKeyFactory(name='test_fk', short_name='test_fk')

        form_data = {'name': 'TEST',
                     'registered_subject': registered_subject.pk,
                     'test_foreign_key': test_fk.pk,
                     'test_many_to_many': test_m2m}
        form = TestSubjectUuidModelForm(data=form_data)
        form.full_clean()
        self.assertFalse(form.is_valid())
