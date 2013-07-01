from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsentedUuidModel
from bhp_base_model.models import TestForeignKey, TestManyToMany
from bhp_off_study.mixins import OffStudyMixin
from bhp_off_study.models import TestOffStudy


class SubjectOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        return TestOffStudy


class TestSubjectUuidModel(SubjectOffStudyMixin, BaseConsentedUuidModel):

    name = models.CharField(max_length=10)

    registered_subject = models.OneToOneField(RegisteredSubject)

    test_foreign_key = models.ForeignKey(TestForeignKey)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

    objects = models.Manager()

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.created

    class Meta:
        app_label = 'bhp_base_test'
