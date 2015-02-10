from uuid import uuid4

from django.db.models import get_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from edc.core.crypto_fields.utils import mask_encrypted
from edc.map.classes import site_mappers

from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household_member.constants import CLINIC_RBD
from apps.bcpp_household_member.models import HouseholdMember

from apps.bcpp_clinic.managers import ClinicHouseholdMemberManager


class ClinicHouseholdMember(HouseholdMember):
    """A proxy model of bcpp_subject.HouseholdMember that bypasses a few features of the
    concrete model."""

    objects = ClinicHouseholdMemberManager()

#     @property
#     def skip_eligible_representative_filled(self):
#         return True

    def save(self, *args, **kwargs):
        """Saves instance but skips proxy model save."""
        update_fields = kwargs.get('update_fields', [])
        if update_fields == ['member_status', 'enrollment_loss_completed']:
            pass
        else:
            # add to the constraint of first_name, initials, household_structure
            # to accept duplicate first_name, initials, household_structure
            # in the clinic. See unique_together.
            self.eligible_member = self.is_eligible_member
            self.member_status = CLINIC_RBD
            self.absent = False
            self.undecided = False
            #if not self.id:
            #    mapper_instance = site_mappers.current_mapper()
            #    clinic_plot = mapper_instance.clinic_plot
            #    self.household_structure = HouseholdStructure.objects.get(
            #        household__plot__plot_identifier=clinic_plot.plot_identifier,
            #        survey__survey_slug=mapper_instance.current_survey_slug)
        super(HouseholdMember, self).save(*args, **kwargs)
        #HouseholdMember.objects.get(pk=self.pk).save(skip_eligible_representative_filled=True)

    def serialize_proxy(self):
        return True

    def __unicode__(self):
        return '{0} {1} {2}{3} {4}'.format(
            mask_encrypted(self.first_name),
            self.initials,
            self.age_in_years,
            self.gender,
            'non-BHS')

    class Meta:
        proxy = True
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Household Member'
        verbose_name_plural = 'Clinic Household Member'
