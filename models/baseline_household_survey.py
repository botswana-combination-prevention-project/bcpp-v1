from django.db import models
from django.core.urlresolvers import reverse
# from django.core.validators import MaxValueValidator, MinValueValidator
from bhp_base_model.fields import OtherCharField
from audit_trail.audit import AuditTrail
from base_scheduled_visit_model import BaseScheduledVisitModel
from bcpp_list.models import ElectricalAppliances, TransportMode
from bcpp_subject.choices import FLOORING_TYPE, WATER_SOURCE, ENERGY_SOURCE, TOILET_FACILITY, SMALLER_MEALS


class BaselineHouseholdSurvey (BaseScheduledVisitModel):
    
    """CS001"""
    
    flooring_type = models.CharField(
        verbose_name="1. What is the main type of flooring for this household?",
        max_length=20,
        choices=FLOORING_TYPE,
        help_text="",
        )
    flooring_type_other = OtherCharField()
    
    living_rooms = models.IntegerField(
        verbose_name=("2.How many living rooms are there in this household unit"
                      " (exclude garage, bathroom, kitchen, store-room, etc if not used as living room )? "),
        max_length=2,
        null=True,
        blank=True,
        help_text=("Note: Record the number of rooms where people live/meet/sleep. If participant does not"
                   " want to answer, leave blank"),
        )
    water_source = models.CharField(
        verbose_name="3. What is the main source of drinking water for this household? ",
        max_length=24,
        choices=WATER_SOURCE,
        help_text="",
        )
    water_source_other = OtherCharField()
    
    energy_source = models.CharField(
        verbose_name="4. What is the main source of energy used for cooking? ",
        max_length=20,
        choices=ENERGY_SOURCE,
        help_text="",
        )
    toilet_facility = models.CharField(
        verbose_name="5. What is the main toilet facility used in this household? ",
        max_length=28,
        choices=TOILET_FACILITY,
        help_text="",
        )
    electrical_appliances= models.ManyToManyField(ElectricalAppliances, 
        verbose_name=("6.Does any member of this household have any of the following that are"
                      " currently working? "),
        null=True,
        blank=True,
        help_text=("(check all that apply). "
                   "Note: Please read each response to the participant and check all that apply. "
                   "If participant does not want to answer, leave blank."),
        )
    transport_mode = models.ManyToManyField(TransportMode,
        verbose_name=("7. Does any member of this household (excluding visitors) own any of the"
                      " following forms of transport in working condition?"),
        null=True,
        blank=True,
        help_text=("(check all that apply). "
                   "Note: Please read each response to the participant and check all that apply. "
                   "If participant does not want to answer, leave blank."),
        )
    goats_owned = models.IntegerField(
        verbose_name=("8. How many goats are owned by the members of this household?"
                      " [If unsure of exact number, give your best guess] "),
        max_length=3,
        null=True,
        blank=True,
        help_text=("Note: May need to assist in adding up goats between household members"
                   " or helping estimate. If resident does not want to answer, leave blank."),
        )
    sheep_owned = models.IntegerField(
        verbose_name=("9.How many sheep are owned by the members of this household?"
                      " [If unsure of exact number, give your best guess] "),
        max_length=3,
        null=True,
        blank=True,
        help_text=("Note: May need to assist in adding up sheep between household members"
                   " or helping estimate. If resident does not want to answer, leave blank."),
        )
    cattle_owned = models.CharField(
        verbose_name=("10. How many head of cattle (cows and bulls) are owned by the members"
                      " of this household? [If unsure of exact number, give your best guess] "),
        max_length=3,
        null=True,
        blank=True,
        help_text=("Note: May need to assist in adding up cows and bulls between household members"
                   " or helping estimate. If resident does not want to answer, leave blank."),
        )
    smaller_meals = models.CharField(
        verbose_name=("11. In the past 4 weeks, did you or any household member have to eat a"
                      " smaller meal than you felt you needed because there was not enough food? "),
        max_length=20,
        choices=SMALLER_MEALS,
        help_text="",
        )
   
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_baselinehouseholdsurvey_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Household Survey Baseline"
        verbose_name_plural = "Household Survey Baseline"
