from django.test import TestCase
from bhp_registration.models import RegisteredSubject
from bhp_base_model.models import TestManyToMany, TestForeignKey
from bhp_consent.forms import TestSubjectUuidModelForm
from base_methods import BaseMethods


class FormsTests(TestCase, BaseMethods):

    def setUp(self):
        self.create_study_variables()
        self.prepare_consent_catalogue()

    def test_base_consented_model_form(self):
        subject_consent = self.create_consent()
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        test_m2m = TestManyToMany.objects.create(name='test_m2m', short_name='test_m2m')
        test_fk = TestForeignKey.objects.create(name='test_fk', short_name='test_fk')

        form_data = {'name': 'TEST',
                     'registered_subject': registered_subject.pk,
                     'test_foreign_key': test_fk.pk,
                     'test_many_to_many': test_m2m}
        form = TestSubjectUuidModelForm(data=form_data)
        #print form.errors
        #self.assertEqual(form.is_valid(), True)
