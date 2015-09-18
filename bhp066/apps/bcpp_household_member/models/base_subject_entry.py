from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.device.sync.models import BaseSyncUuidModel
from edc_base.encrypted_fields import EncryptedCharField, EncryptedTextField
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_before_study_start, date_not_future

from bhp066.apps.bcpp_household.models import Plot

from .base_member_status_model import BaseMemberStatusModel

from ..choices import NEXT_APPOINTMENT_SOURCE


class BaseSubjectEntry(BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """For absentee and undecided log models."""
    report_datetime = models.DateField(
        verbose_name="Report date",
        validators=[date_not_before_study_start, date_not_future])

    reason_other = OtherCharField()

    next_appt_datetime = models.DateTimeField(
        verbose_name=_("Follow-up appointment"),
        help_text=_("The date and time to meet with the subject"))

    next_appt_datetime_source = models.CharField(
        verbose_name=_("Appointment date suggested by?"),
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text='')

    contact_details = EncryptedCharField(
        null=True,
        blank=True,
        help_text=_('Information that can be used to contact someone, '
                    'preferrably the subject, to confirm the appointment'))

    comment = EncryptedTextField(
        verbose_name="Comments",
        max_length=250,
        blank=True,
        null=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment'))

    @property
    def in_replaced_household(self):
        """Returns True if the household for this entry is "replaced"""""
        return self.inline_parent.household_member.household_structure.household.replaced_by

    def dispatch_container_lookup(self):
        field = None
        for fld in self._meta.fields:
            if fld.rel:
                if issubclass(fld.rel.to, BaseMemberStatusModel):
                    field = fld
                    break
        if not field:
            raise TypeError('Method \'dispatch_container_lookup\' cannot find the "inline\'s" '
                            'related field for class {0}'.format(self.__class__))
        return (Plot, ('{0}__household_member__household_structure__household__'
                       'plot__plot_identifier').format(field.name))

    class Meta:
        abstract = True
