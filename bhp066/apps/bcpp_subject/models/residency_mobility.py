from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail

from apps.bcpp.choices import YES_NO_DWTA, YES_NO, LENGTHRESIDENCE_CHOICE, NIGHTSAWAY_CHOICE, CATTLEPOSTLANDS_CHOICE, COMMUNITIES
from .base_scheduled_visit_model import BaseScheduledVisitModel


class ResidencyMobility (BaseScheduledVisitModel):

    """CS002"""

    length_residence = models.CharField(
        verbose_name=_('How long have you lived in this community?'),
        max_length=25,
        choices=LENGTHRESIDENCE_CHOICE,
        help_text="",
        )

    permanent_resident = models.CharField(
        verbose_name=_("In the past 12 months, have you typically spent 14 or"
                      " more nights per month in this community? "),
        max_length=10,
        choices=YES_NO_DWTA,
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent more than 14 nights per month in this community. "
                  "If 'NO (or don't want to answer)' STOP. Participant cannot be enrolled."),
        )

    intend_residency = models.CharField(
        verbose_name=_("Do you intend to move out of the community in the next 12 months?"),
        max_length=25,
        choices=YES_NO,
        help_text="",
        )

    # see redmine 423 and 401 and 126
    nights_away = models.CharField(
        verbose_name=_("In the past 12 months, in total how many nights did you spend away"
                      " from this community, including visits to cattle post and lands?"
                      "[If you don't know exactly, give your best guess]"),
        max_length=35,
        choices=NIGHTSAWAY_CHOICE,
        help_text="",
        )

    cattle_postlands = models.CharField(
        verbose_name=_("In the past 12 months, during the times you were away from this community, "
                      "where were you primarily staying?"),
        max_length=25,
        choices=CATTLEPOSTLANDS_CHOICE,
        default='N/A',
        help_text="",
        )
    cattle_postlands_other = models.CharField(
        verbose_name=_("Give the name of the community"),
        max_length=65,
        choices=COMMUNITIES,
        null=True,
        blank=True,
        help_text="",
        )

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.subject_visit)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Residency & Mobility"
        verbose_name_plural = "Residency & Mobility"
