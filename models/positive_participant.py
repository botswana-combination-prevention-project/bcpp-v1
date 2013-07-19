from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import AGREE_STRONGLY
from base_scheduled_visit_model import BaseScheduledVisitModel


class PositiveParticipant (BaseScheduledVisitModel):
    
    """CS002"""
    
    """Interviewer Note: The following supplemental questions are only asked for"
    "respondents with known HIV infection. SKIP for respondents without known HIV infection. """
    
    internalize_stigma = models.CharField(
        verbose_name=_("I think less of myself."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    internalized_stigma = models.CharField(
        verbose_name=_("I have felt ashamed because of having HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    friend_stigma = models.CharField(
        verbose_name=_("I fear that if I disclosed my HIV status to my"
                      " friends, they would lose respect for me."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    family_stigma = models.CharField(
        verbose_name=_("I fear that if I disclosed my HIV status to my family,"
                      " they would exclude me from usual family activities."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_talk_stigma = models.CharField(
        verbose_name=_("People have talked badly about me."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_respect_stigma = models.CharField(
        verbose_name=_("I have lost respect or standing in the community."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_jobs_tigma = models.CharField(
        verbose_name=_("I have lost a job because of having HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_positiveparticipant_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Positive Participant"
        verbose_name_plural = "Positive Participant"
