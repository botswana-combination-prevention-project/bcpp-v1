from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bcpp_list.models import NeighbourhoodProblems
from bcpp.choices import COMMUNITYENGAGEMENT_CHOICE, VOTEENGAGEMENT_CHOICE, SOLVEENGAGEMENT_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class CommunityEngagement (BaseScheduledVisitModel):

    """CS002"""
    
    community_engagement = models.CharField(
        verbose_name="CE1. How active are you in community activities such as celebrations, health campaigns and development of the community that surrounds you??",
        max_length=25,
        choices=COMMUNITYENGAGEMENT_CHOICE,
        help_text="",
        )

    vote_engagement = models.CharField(
        verbose_name="CE2. Did you vote in the last local government election?",
        max_length=25,
        choices=VOTEENGAGEMENT_CHOICE,
        help_text="",
        )

    problems_engagement = models.ManyToManyField(NeighbourhoodProblems,
        verbose_name="CE3. What are the major problems in this neighbourhood??",
        help_text=("Note:Interviewer to read question but NOT the responses. Check the boxes of"
                   " any of problems mentioned."),
        )
    problems_engagement_other = OtherCharField()

    solve_engagement = models.CharField(
        verbose_name="CE4. If there is a problem in this neighbourhood, do the adults work together in solving it?",
        max_length=25,
        choices=SOLVEENGAGEMENT_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Community Engagement"
        verbose_name_plural = "Community Engagement"
