from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp_list.models import NeighbourhoodProblems
from bcpp.choices import COMMUNITYENGAGEMENT_CHOICE, VOTEENGAGEMENT_CHOICE, SOLVEENGAGEMENT_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class CommunityEngagement (BaseScheduledVisitModel):
    
    """CS002"""
    
    communityengagement = models.CharField(
        verbose_name = "CE1. How active are you in community activities such as celebrations, health campaigns and development of the community that surrounds you??",
        max_length = 15,
        choices = COMMUNITYENGAGEMENT_CHOICE,
        help_text="",
        )

    voteengagement = models.CharField(
        verbose_name = "CE2. Did you vote in the last local government election?",
        max_length = 15,
        choices = VOTEENGAGEMENT_CHOICE,
        help_text="",
        )

    problemsengagement = models.ManyToManyField(NeighbourhoodProblems,
        verbose_name = "CE3. What are the major problems in this neighbourhood??",
        max_length = 25,
        help_text=("Note:Interviewer to read question but NOT the responses. Check the boxes of"
                   " any of problems mentioned."),
        )

    solveengagement = models.CharField(
        verbose_name = "CE4. If there is a problem in this neighbourhood, do the adults work together in solving it?",
        max_length = 15,
        choices = SOLVEENGAGEMENT_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_communityengagement_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Community Engagement"
        verbose_name_plural = "Community Engagement"
