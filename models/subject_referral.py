from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bhp_base_model.validators import datetime_is_future
from bhp_common.choices import YES_NO
from bhp_appointment_helper.models import BaseAppointmentMixin
from bcpp_subject.choices import REFERRAL_REASONS
from base_registered_household_member_model import BaseRegisteredHouseholdMemberModel


class SubjectReferral(BaseRegisteredHouseholdMemberModel, BaseAppointmentMixin):
    
    subject_referral_reason = models.CharField(
        verbose_name="Reason for referral",
        max_length=40,
        choices=REFERRAL_REASONS,
        help_text=""
        )
    subject_referral_reason_other = OtherCharField()
    
    next_appt_datetime = models.DateTimeField(
        verbose_name="Clinic appointment date and time",
        validators=[datetime_is_future, ],
        null=True,
        blank=True,
        help_text=""
        )
    referral_result = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        editable=False
        )
    in_clinic = models.CharField(
        max_length=10,
        choices=YES_NO,
        default='No',
        editable=False
        )
    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment')
        )
    
    objects = models.Manager()

    history = AuditTrail()
    
    def __unicode__(self):
        return unicode(self.household_member)

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(SubjectReferral, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectreferral_change', args=(self.id,))

    class Meta:
        ordering = ['household_member']
        app_label = 'bcpp_subject'
        verbose_name = 'Subject Referral'
