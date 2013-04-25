from datetime import datetime
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from bhp_base_model.fields import OtherCharField
from bhp_registration.models import BaseRegisteredSubjectModel
from bhp_crypto.utils import mask_encrypted
from bhp_off_study.managers import OffStudyManager


class BaseOffStudy(BaseRegisteredSubjectModel):

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        help_text="",
        )

    reason = models.CharField(
        verbose_name="Please code the primary reason participant taken off-study",
        max_length=30,
        # choices = OFF_STUDY_REASON,
        )

    reason_other = OtherCharField()

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments:",
        blank=True,
        null=True,
        )

    objects = OffStudyManager()

    def natural_key(self):
        return (self.offstudy_date, ) + self.registered_subject.natural_key()

    def get_report_datetime(self):
        return datetime(self.offstudy_date.year, self.offstudy_date.month, self.offstudy_date.day)

#    def get_visit_model(self):
#        """Returns the visit model class from the app needed to clear appointments on save().
#
#        Users should override to return the visit model relavant to the
#        off study form."""
#        return None

    def post_save(self):
        """Deletes appointments created after the off-study datetime if the appointment has no visit report."""
        Appointment = models.get_model('bhp_appointment', 'appointment')
        visit_model_cls = self.get_visit_model_cls()
        if not visit_model_cls:
            raise ImproperlyConfigured('Model {0} cannot determine the visit model class for the app'.format(self._meta.object_name))
        if visit_model_cls:
            for appointment in Appointment.objects.filter(
                    registered_subject=self.registered_subject,
                    appt_datetime__gt=self.offstudy_date):
                # only delete appointments that have no visit report
                if not visit_model_cls.objects.filter(appointment=appointment).exists():
                    appointment.delete()

    def __unicode__(self):
        return "{0} {1} ({2})".format(self.registered_subject.subject_identifier,
                                      self.registered_subject.subject_type,
                                      mask_encrypted(self.registered_subject.first_name))

    class Meta:
        app_label = 'bhp_off_study'
        abstract = True
