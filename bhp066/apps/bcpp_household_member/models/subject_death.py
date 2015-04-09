from datetime import datetime

from django.db import models

from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.audit.audit_trail import AuditTrail
from edc.subject.adverse_event.models import BaseDeath

from apps.bcpp_survey.models import Survey

from .base_member_status_model import BaseMemberStatusModel
from .household_member import HouseholdMember


class SubjectDeath(BaseDeath):

    history = AuditTrail()
    
    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today())

    survey = models.ForeignKey(Survey, editable=False)

    def __unicode__(self):
        return unicode(self.registered_subject)

    def get_report_datetime(self):
        return self.report_datetime

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_member__household_structure__household__plot')

    def natural_key(self):
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_member__household_structure__household__plot__plot_identifier')

    def is_dispatchable(self):
        return True

    def get_registration_datetime(self):
        return self.report_datetime

    def confirm_registered_subject_pk_on_post_save(self, using):
        if self.registered_subject.pk != self.household_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_member.'
                            'registered_subject.pk. Got {0} != {1}.'.format(
                                self.registered_subject.pk, self.household_member.registered_subject.pk))

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Subject Death"
        verbose_name_plural = "Subject Death"
