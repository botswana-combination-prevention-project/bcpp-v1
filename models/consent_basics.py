from django.db import models
from bhp_subject.models import BaseSubject
from bhp_common.choices import YES_NO
from bhp_base_model.validators import eligible_if_yes


class ConsentBasics(BaseSubject):
    """Adds questions to confirm the consent process was followed."""
    
    consent_reviewed = models.CharField(
        verbose_name="I have reviewed the consent with the client",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=True,
        default='Yes',
        help_text="If no, INELIGIBLE",
        )
    study_questions= models.CharField(
        verbose_name="I have answered all questions the client had about the study",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=True,
        default='Yes',
        help_text="If no, INELIGIBLE",
        )
    assessment_score = models.CharField(
        verbose_name=("The client has completed the assessment of understanding with a"
                      " passing score"),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=True,
        default='Yes',
        help_text="If no, INELIGIBLE",
        )
    consent_copy = models.CharField(
        verbose_name=("I have provided the client with a copy of their signed informed"
                      " consent"),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=True,
        default='Yes',
        help_text="If no, INELIGIBLE",
        )

    class Meta:
        abstract = True

