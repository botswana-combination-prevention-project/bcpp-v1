from django.db import models
from django.db.models import get_model
from django.contrib import messages
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.choices.common import YES_NO

from apps.bcpp_household.models import HouseholdStructure

from ..managers import HouseholdHeadEligibilityManager
from .household_member import HouseholdMember


class HouseholdHeadEligibility(BaseDispatchSyncUuidModel):
    """Determines if the household member is eligible to be treated as head of houehold."""
    household_structure = models.ForeignKey(HouseholdStructure)

    household_member = models.OneToOneField(HouseholdMember,
        help_text=('Important: The household member must verbally consent before completing this questionnaire.'))

    report_datetime = models.DateTimeField(
        verbose_name="Report Date/Time",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    aged_over_18 = models.CharField(
        verbose_name=("Did you verify that the respondent is aged 18 or older? "),
        max_length=10,
        choices=YES_NO,
        help_text=("If under 18 participant cannot be head of household."),
        )

    verball_script = models.CharField(
        verbose_name=("Did you administer the verbal script and ensure the respondent is willing "
                      "to provide household information? "),
        max_length=10,
        choices=YES_NO,
        help_text=("If No the participant cannot be head of household."),
        )

    objects = HouseholdHeadEligibilityManager()

    history = AuditTrail()

    def __unicode__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError("household_member cannot be None for household_head_eligibility with pk='\{0}\'".format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    def dispatch_container_lookup(self, using=None):
        return (get_model('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        if self.aged_over_18.lower() == 'yes' and self.household_member.age_in_years < 18:
            raise TypeError('This household member\'s is recorded to be less than 18. Its \'{0}\'. But in this form you say they are 18 or older. Please correct.'.format(self.household_member.age_in_years))
        if self.aged_over_18.lower() == 'no' or self.verball_script.lower() == 'no':
            self.household_member.eligible_hoh = False
#             messages.add_message(request, messages.ERROR, '')
        else:
            self.household_member.eligible_hoh = True
        self.household_member.save()
        super(HouseholdHeadEligibility, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
