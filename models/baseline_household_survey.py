from django.db import models
from bhp_base_model.fields import OtherCharField
from audit_trail.audit import AuditTrail
from base_scheduled_visit_model import BaseScheduledVisitModel
from bcpp_list.models import ElectricalAppliances, TransportMode
from bcpp_subject.choices import FLOORING_TYPE, WATER_SOURCE, ENERGY_SOURCE, TOILET_FACILITY, SMALLER_MEALS


class BaselineHouseholdSurvey (BaseScheduledVisitModel):

    """CS001"""

    flooring_type = models.CharField(
        verbose_name="What is the main type of flooring for this household?",
        max_length=25,
        choices=FLOORING_TYPE,
        help_text="",
        )
    flooring_type_other = OtherCharField()

    living_rooms = models.IntegerField(
        verbose_name=("How many living rooms are there in this household unit"
                      " (exclude garage, bathroom, kitchen, store-room, etc if not used as living room )? "),
        max_length=2,
        null=True,
        blank=True,
        help_text=("Note: Record the number of rooms where people live/meet/sleep. If participant does not"
                   " want to answer, leave blank"),
        )
    water_source = models.CharField(
        verbose_name="What is the main source of drinking water for this household? ",
        max_length=35,
        choices=WATER_SOURCE,
        help_text="",
        )
    water_source_other = OtherCharField()

    energy_source = models.CharField(
        verbose_name="What is the main source of energy used for cooking? ",
        max_length=35,
        choices=ENERGY_SOURCE,
        help_text="",
        )
    energy_source_other = OtherCharField()

    toilet_facility = models.CharField(
        verbose_name="What is the main toilet facility used in this household? ",
        max_length=35,
        choices=TOILET_FACILITY,
        help_text="",
        )
    toilet_facility_other = OtherCharField()

    electrical_appliances = models.ManyToManyField(ElectricalAppliances,
        verbose_name=("Does any member of this household have any of the following that are"
                      " currently working? (check all that apply)."),
        null=True,
        blank=True,
        help_text=("Note: Please read each response to the participant and check all that apply. "
                   "If participant does not want to answer, leave blank."),
        )
    transport_mode = models.ManyToManyField(TransportMode,
        verbose_name=("Does any member of this household (excluding visitors) own any of the"
                      " following forms of transport in working condition? (check all that apply)."),
        null=True,
        blank=True,
        help_text=("Note: Please read each response to the participant and check all that apply. "
                   "If participant does not want to answer, leave blank."),
        )
    goats_owned = models.IntegerField(
        verbose_name=("How many goats are owned by the members of this household?"
                      " [If unsure of exact number, give your best guess] "),
        max_length=3,
        null=True,
        blank=True,
        help_text=("Note: May need to assist in adding up goats between household members"
                   " or helping estimate. If resident does not want to answer, leave blank."),
        )
    sheep_owned = models.IntegerField(
        verbose_name=("How many sheep are owned by the members of this household?"
                      " [If unsure of exact number, give your best guess] "),
        max_length=3,
        null=True,
        blank=True,
        help_text=("Note: May need to assist in adding up sheep between household members"
                   " or helping estimate. If resident does not want to answer, leave blank."),
        )
    cattle_owned = models.IntegerField(
        verbose_name=("How many head of cattle (cows and bulls) are owned by the members"
                      " of this household? [If unsure of exact number, give your best guess] "),
        max_length=3,
        null=True,
        blank=True,
        help_text=("Note: May need to assist in adding up cows and bulls between household members"
                   " or helping estimate. If resident does not want to answer, leave blank."),
        )
    smaller_meals = models.CharField(
        verbose_name=("In the past 4 weeks, did you or any household member have to eat a"
                      " smaller meal than you felt you needed because there was not enough food? "),
        max_length=25,
        choices=SMALLER_MEALS,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Household Survey Baseline"
        verbose_name_plural = "Household Survey Baseline"
