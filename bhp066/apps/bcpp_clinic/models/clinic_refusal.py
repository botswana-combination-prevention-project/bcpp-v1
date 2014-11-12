from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import date_not_future, date_not_before_study_start
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.map.classes import site_mappers

from apps.bcpp_household_member.models import HouseholdMember


class ClinicRefusal(BaseDispatchSyncUuidModel):
    "A model completed by the user for eligible participants who decide not to participate."""
    household_member = models.OneToOneField(HouseholdMember, null=True)

    refusal_date = models.DateField(
        verbose_name=_("Date subject refused participation"),
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")

    community = models.CharField(max_length=25, editable=False)

    reason = models.CharField(
        verbose_name=_("We respect your decision to decline. It would help us"
                       " improve the study if you could tell us the main reason"
                       " you do not want to participate in this study?"),
        max_length=50,
        choices=(('dont_want', 'I don\'t want to take part'),
                 ('not_sure', 'I am not sure'),
                 ('dont_want_blood_draw', 'I don\'t want to have blood drawn'),
                 ('needles_phobia', 'Fear of needles'),
                 ('privacy', 'I am afraid my information will not be private'),
                 ('illiterate no witness', 'Illiterate does not want a witness'),
                 ('on_haart', 'Already on HAART'),
                 ('knows_status', 'I already know my status'),
                 ('OTHER', 'Other, specify')),
        help_text="")

    reason_other = OtherCharField()

    comment = models.CharField(
        verbose_name=_("Comment"),
        max_length=250,
        null=True,
        blank=True,
        help_text=_('IMPORTANT: Do not include any names or other personally identifying '
                    'information in this comment'))

    history = AuditTrail()

    def __unicode__(self):
        return "for participant"

    def save(self, *args, **kwargs):
        self.community = site_mappers.get_current_mapper().map_area
        super(ClinicRefusal, self).save(*args, **kwargs)

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = 'Clinic Refusal'
