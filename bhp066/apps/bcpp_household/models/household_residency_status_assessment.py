from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO, YES_NO_DONT_KNOW, RESIDENT_LAST_SEEN
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_list.models import ResidentMostLikely
from apps.bcpp_household.managers import HouseholdResidencyStatusAssessmentManager

from .household import Household
from .plot import Plot


class HouseholdResidencyStatusAssessment(BaseDispatchSyncUuidModel):

    household = models.ForeignKey(Household, null=True)

    residency = models.CharField(
        verbose_name='Is anybody living in this Household?',
        choices=YES_NO,
        max_length=25,
        null=True,
        editable=True,
        )

    member_count = models.IntegerField(
        verbose_name="How many people live in this household (estimate)?",
        null=True,
        blank=True,
        help_text=("Provide the number of members in this household."))

    citizen = models.CharField(
        verbose_name='Is anyone in this household a Motswana?',
        choices=YES_NO_DONT_KNOW,
        max_length=25,
        null=True,
        blank=True,
        editable=True,
        )

    how_many = models.IntegerField(
        verbose_name="If answer to question 3 is yes, how many?",
        null=True,
        help_text=("Provide the number of members in this household who are Batswana."),
        blank=True)

    possible_eligibles = models.CharField(
        verbose_name='Is there anyone among the Batswana in this household between the ages 16-64 years?',
        choices=YES_NO_DONT_KNOW,
        max_length=25,
        null=True,
        blank=True,
        editable=True,
        )

    how_many_members = models.IntegerField(
        verbose_name="If answer to question above is yes, how many?",
        null=True,
        help_text=("Provide the number of members  aged between 16-64 this household who are Batswana."),
        blank=True)

    original_community = models.CharField(
        verbose_name='Is this person originally from this community? [A motho yo o tlholega mo motseng o?]',
        choices=YES_NO_DONT_KNOW,
        max_length=25,
        null=True,
        blank=True,
        editable=True,
        )

    original_community_other = models.CharField(
        verbose_name='If the answer to above is No, specify the community where the person originates from.',
        max_length=25,
        null=True,
        blank=True,
        editable=True,
        )

    last_seen_home = models.CharField(
        verbose_name='When was a resident last seen in this household?',
        choices=RESIDENT_LAST_SEEN,
        max_length=25,
        null=True,
        blank=True,
        editable=True,
        )

    most_likely = models.ManyToManyField(ResidentMostLikely,
        verbose_name=_("Which of the following do you think is most likely? household resident is"),
        null=True,
        blank=True,
        help_text=("Note: Please read each response to the participant and check all that apply. "
                   "If participant does not want to answer, leave blank."),
        )

    def __unicode__(self):
        return unicode(self.household)

    objects = HouseholdResidencyStatusAssessmentManager()

    history = AuditTrail()

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_household.household']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household__plot__plot_identifier')

    @property
    def vdc_househould_status(self):
        status = None
        seasonal = ['work_live_school_outside_village', 'away_for_harvesting']
        rarely_there = ['work_live_school_outside', 'work_live_school_elsewhere']
        never_there = ['dead', 'moved_away_permanently']
        most_likely = []
        for item in self.most_likely.all():
            most_likely.append(item.short_name)
        if most_likely:
            if self.compare_list(most_likely, seasonal):
                status = 'seasonally_there'
            elif self.compare_list(most_likely, rarely_there):
                status = 'rarely_there'
            elif self.compare_list(most_likely, never_there):
                status = 'never_there'
        return status

    def compare_list(self, l1, l2):
        i,j = 0,len(l1)
        for e in l2:
            if e == l1[i]:
                i += 1
            if i == j:
                return True
        return False

    class Meta:
        app_label = 'bcpp_household'
        verbose_name = 'Household Residency Status Assess'
        verbose_name_plural = 'Household Residency Status Assess'
