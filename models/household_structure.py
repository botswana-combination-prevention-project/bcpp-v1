from django.db import models
from django.db.models import get_model
from django.core.validators import MinValueValidator, MaxValueValidator
from audit_trail.audit import AuditTrail
from bcpp_survey.models import Survey
from bcpp_household.managers import HouseholdStructureManager
from household import Household
from base_uuid_model import BaseUuidModel


class HouseholdStructure(BaseUuidModel):

    """ Each year/survey a new household_structure is created for the household """

    household = models.ForeignKey(Household)

    survey = models.ForeignKey(Survey)

    member_count = models.IntegerField(
        verbose_name="How many members in this household?",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(50), ],
        help_text="This is the total number of members in the household. You may change this later.",
            )
    note = models.CharField("Note", max_length=250, blank=True)

    objects = HouseholdStructureManager()

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.household)

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_survey.survey', 'bcpp_household.household', ]

    def gps_point(self):
        return "LON:%s LAT:%s" % (self.household.gps_point_11, self.household.gps_point_21)

    def get_absolute_url(self):
        return "/admin/bcpp_household/householdstructure/%s/" % self.id

    def calendar_datetime(self):
        return self.created

    def calendar_label(self):
        return self.__unicode__()

    def group_permissions(self):
        return {'survey': ('add', 'change')}

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household__household_identifier')

    def get_subject_identifier(self):
        #subject_identifier = self.household.household_identifier
        return self.household.household_identifier

    def fetch_and_count_members_on_post_save(self, **kwargs):
        """Fetches members from the previous survey, if new, and checks the number of members."""
        created = kwargs.get('created', False)
        using = kwargs.get('using', None)
        # create new members, if new
        if created:
            self.__class__.objects.fetch_household_members(self, using)
        # recount members, may be greater but not less than the actual number of members
        household_structure_member = get_model(app_label="bcpp_household", model_name="householdstructuremember")
        current_member_count = household_structure_member.objects.filter(household_structure=self).count()
        self.member_count = self.member_count or 0
        if self.member_count < current_member_count:
            self.member_count = current_member_count
            # count has changed or was incorrect, so update
            self.save(using=using)

    class Meta:
        app_label = 'bcpp_household'
        unique_together = (('household', 'survey'), )
