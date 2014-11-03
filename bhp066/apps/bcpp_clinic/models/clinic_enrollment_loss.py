from django.db import models

from edc.audit.audit_trail import AuditTrail

from .base_clinic_registered_subject_model import BaseClinicRegisteredSubjectModel


class ClinicEnrollmentLoss(BaseClinicRegisteredSubjectModel):

    reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Do not include any personal identifiable information.'
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        super(ClinicEnrollmentLoss, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.registered_subject)

    class Meta:
        app_label = 'bcpp_clinic'
