from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import COMMUNITYENGAGEMENT_CHOICE, VOTEENGAGEMENT_CHOICE, SOLVEENGAGEMENT_CHOICE
from bhp066.apps.bcpp_list.models import NeighbourhoodProblems

from .base_scheduled_visit_model import BaseScheduledVisitModel


class CommunityEngagement (BaseScheduledVisitModel):

    community_engagement = models.CharField(
        verbose_name=_("How active are you in community activities such as"
                       " burial society, Motshelo, Syndicate, PTA, "
                       "VDC(Village Developement Committee), Mophato"
                       " and development of the community that surrounds you??"),
        max_length=25,
        null=True,
        choices=COMMUNITYENGAGEMENT_CHOICE,
        help_text="supplemental")

    vote_engagement = models.CharField(
        verbose_name=_("Did you vote in the last local government election?"),
        max_length=50,
        null=True,
        choices=VOTEENGAGEMENT_CHOICE,
        help_text="supplemental")

    problems_engagement = models.ManyToManyField(
        NeighbourhoodProblems,
        verbose_name=_("What are the major problems in this neighbourhood??"),
        null=True,
        help_text=("supplemental. Note:Interviewer to read question but NOT the responses. Check the boxes of"
                   " any of problems mentioned."))

    problems_engagement_other = OtherCharField(
        null=True,)

    solve_engagement = models.CharField(
        verbose_name=_("If there is a problem in this neighbourhood, do the"
                       " adults work together in solving it?"),
        max_length=25,
        null=True,
        choices=SOLVEENGAGEMENT_CHOICE,
        help_text="supplemental")

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Community Engagement"
        verbose_name_plural = "Community Engagement"
