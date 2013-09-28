from django.db import models
from django.utils.translation import ugettext as _
from edc_lib.audit_trail.audit import AuditTrail
from edc_lib.bhp_base_model.fields import OtherCharField
from bcpp.choices import YES_NO_REFUSED
from bcpp_subject.choices import CARE_FACILITIES, CARE_REASON, TRAVEL_HOURS
from base_scheduled_visit_model import BaseScheduledVisitModel


class OutpatientCare (BaseScheduledVisitModel):

    """CE001- Resource Utilization sub"""

    govt_health_care = models.CharField(
        verbose_name=_("In the last 3 months, did you seek care at a Government Primary"
                  " Health Clinic/Post? Not including any visits for which you were hospitalized. "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    dept_care = models.CharField(
        verbose_name=_("In the last 3 months, did you seek care at a Hospital Outpatient Department,"
                  " including Govt, private and church/mission hospitals? Not including any visits"
                  " for which you were hospitalized. "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    prvt_care = models.CharField(
        verbose_name=_("In the last 3 months, did you seek care from a Private Doctor? "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    trad_care = models.CharField(
        verbose_name=_("In the last 3 months, did you seek care from a Traditional or Faith Healer? "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    care_visits = models.IntegerField(
        verbose_name=_("In the last 3 months, how many total outpatient visits have"
                      " you to all of the above places? "),
        max_length=2,
        null=True,
        blank=True,
        help_text="Note:If participant does not want to answer, leave blank.",
        )
    facility_visited = models.CharField(
        verbose_name=_("For the most recent outpatient medical care visit in the past 3 months, which"
                  " type of facility did you visit? "),
        max_length=65,
        choices=CARE_FACILITIES,
        help_text="if 'NOT Government Primary Health Clinic/Post' go to question Q9. ",
        )

    specific_clinic = models.CharField(
        verbose_name=_("For this most recent visit to a Government Primary Health Clinic/Post, "
                  "which clinic did you visit? "),
        max_length=50,
        null=True,
        blank=True,
        help_text="Note:If participant does not want to answer, leave blank",
        )
    care_reason = models.CharField(
        verbose_name=_("For this most recent medical care visit, what was the primary reason you sought care? "),
        max_length=95,
        choices=CARE_REASON,
        help_text="",
        )
    care_reason_other = OtherCharField()

    outpatient_expense = models.DecimalField(
        verbose_name=_("For this most recent outpatient medical care visit, how much did you have to pay"
                  " to the health care provider, including any medicines?"),
        max_digits=5,
        decimal_places=2,
        help_text="Pula",
        )
    travel_time = models.CharField(
        verbose_name=_("For this most recent outpatient medical care visit, how long did it take you to get"
                  " to the clinic? "),
        max_length=25,
        choices=TRAVEL_HOURS,
        help_text="",
        )
    transport_expense = models.DecimalField(
        verbose_name=_("For this most recent outpatient medical care visit, how much did you have"
                      " to pay for transport, food and accommodation? [include cost for fuel if using"
                      " a private car] "),
        max_digits=5,
        decimal_places=2,
        help_text="Pula",
        )
    cost_cover = models.CharField(
        verbose_name=_("For this most recent outpatient medical care visit, were any of these costs"
                      " by covered by anyone else, such as your medical aid or employer? "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    waiting_hours = models.CharField(
        verbose_name=_("For this most recent outpatient medical care visit, how long did you have"
                      " to wait before you were seen, from when you arrived at the facility? "),
        max_length=25,
        choices=TRAVEL_HOURS,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "RU: Outpatient care"
        verbose_name_plural = "RU: Outpatient care"
