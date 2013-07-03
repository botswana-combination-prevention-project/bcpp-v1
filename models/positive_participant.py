from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import AGREE_STRONGLY
from base_scheduled_visit_model import BaseScheduledVisitModel


class PositiveParticipant (BaseScheduledVisitModel):
    
    """CS002"""
    
    """Interviewer Note: The following supplemental questions are only asked for"
    "respondents with known HIV infection. SKIP for respondents without known HIV infection. """
    
    internalize_stigma = models.CharField(
        verbose_name="Supplemental ST13. I think less of myself.",
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    internalized_stigma = models.CharField(
        verbose_name=("Supplemental ST14. I have felt ashamed because of having HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    friend_stigma = models.CharField(
        verbose_name=("Supplemental ST15. I fear that if I disclosed my HIV status to my"
                      " friends, they would lose respect for me."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    family_stigma = models.CharField(
        verbose_name=("Supplemental ST16. I fear that if I disclosed my HIV status to my family,"
                      " they would exclude me from usual family activities."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    enacted_talk_stigma = models.CharField(
        verbose_name="Supplemental ST17. People have talked badly about me.",
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    enacted_respect_stigma = models.CharField(
        verbose_name=("Supplemental ST18. I have lost respect or standing in the community."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    enacted_jobs_tigma = models.CharField(
        verbose_name=("Supplemental ST19. I have lost a job because of having HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_positiveparticipant_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Positive Participant"
        verbose_name_plural = "Positive Participant"
