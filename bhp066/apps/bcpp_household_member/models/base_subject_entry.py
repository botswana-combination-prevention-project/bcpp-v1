from django.db import models

from edc.base.model.fields import OtherCharField
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.core.crypto_fields.fields import EncryptedCharField
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_household.models import  Plot
from apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel

from ..choices import NEXT_APPOINTMENT_SOURCE


class BaseSubjectEntry(BaseDispatchSyncUuidModel):
    """For absentee and undecided log models."""
    report_datetime = models.DateTimeField("Report date",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    reason_other = OtherCharField()

    next_appt_datetime = models.DateTimeField(
        verbose_name="Follow-up appointment",
        help_text="The date and time to meet with the subject"
        )

    next_appt_datetime_source = models.CharField(
        verbose_name="Appointment date suggested by?",
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text=''
        )

    contact_details = EncryptedCharField(
        null=True,
        blank=True,
        #editable=False,
        help_text=('Information that can be used to contact someone, '
                   'preferrably the subject, to confirm the appointment'),
        )

    comment = EncryptedTextField(
        verbose_name="Comments",
        max_length=250,
        blank=True,
        null=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
           'information in this comment')
        )

    def save(self, *args, **kwargs):
        if self.in_replaced_household:
            raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
        else:
            self.update_replacement_data()
        super(BaseSubjectEntry, self).save(*args, **kwargs)

    @property
    def in_replaced_household(self):
        """Returns True if the household for this entry is "replaced"""""
        return self.inline_parent.household_member.household_structure.household.replaced

    def update_replacement_data(self, using=None):
        plot = self.inline_parent.household_member.household_structure.household.plot
        household = self.inline_parent.household_member.household_structure.household
        household_structure = self.inline_parent.household_member.household_structure
        
        if ReplacementData(household_structure).check_refusals():
            for item in ReplacementData().check_refusals(plot):  # item is a household or a plot
                item[0].replaceble = True
                item[0].save()
        if ReplacementData().check_absentees_ineligibles(plot):
            for item in ReplacementData().check_absentees_ineligibles(plot):
                item[0].replaceble = True
                item[0].save()
        if ReplacementData().is_replacement_valid(plot):
            for item in ReplacementData().is_replacement_valid(plot):
                item[0].replaceble = True
                item[0].save()

    def dispatch_container_lookup(self):
        field = None
        for fld in self._meta.fields:
            if fld.rel:
                if issubclass(fld.rel.to, BaseMemberStatusModel):
                    field = fld
                    break
        if not field:
            raise TypeError('Method \'dispatch_container_lookup\' cannot find the "inline\'s" related field for class {0}'.format(self.__class__))
        return (Plot, '{0}__household_member__household_structure__household__plot__plot_identifier'.format(field.name))

    class Meta:
        abstract = True
