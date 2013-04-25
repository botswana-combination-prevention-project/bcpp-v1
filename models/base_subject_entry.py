from django.db import models
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bhp_crypto.fields import EncryptedCharField
from bhp_base_model.fields import OtherCharField
from bcpp_household.models import Household
from bcpp_subject.choices import NEXT_APPOINTMENT_SOURCE
from base_uuid_model import BaseUuidModel
from base_member_status_model import BaseMemberStatusModel


class BaseSubjectEntry(BaseUuidModel):
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
        editable=False,
        help_text=('Information that can be used to contact someone, '
                   'preferrably the subject, to confirm the appointment'),
        )

    comment = models.TextField(
        verbose_name="Comments",
        max_length=250,
        blank=True,
        null=True,
        editable=False,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
           'information in this comment')
        )

    def dispatch_container_lookup(self):
        field = None
        for fld in self._meta.fields:
            if fld.rel:
                if issubclass(fld.rel.to, BaseMemberStatusModel):
                    field = fld
                    break
        if not field:
            raise TypeError('Method \'dispatch_container_lookup\' cannot find the "inline\'s" related field for class {0}'.format(self.__class__))
        return (Household, '{0}__household_structure_member__household_structure__household__household_identifier'.format(field.name))

    class Meta:
        abstract = True
