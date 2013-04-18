from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.validators import eligible_if_yes
from bhp_common.choices import YES_NO, YES_NO_REFUSED
from bcpp_subject.choices import ENROLMENT_REASON, OPPORTUNISTIC_ILLNESSES
from bhp_registration.models import BaseRegisteredSubjectModel


class CeaEnrolmentChecklist (BaseRegisteredSubjectModel):
    
    """CE003"""
    
    mental_capacity = models.CharField(
        verbose_name=("1. [Interviewer] Does the prospective participant have sufficient"
                      " mental capacity to provide considered informed consent? "),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )
    
    incarceration = models.CharField(
        verbose_name=("2. [Interviewer] Is the prospective participant currently under"
                      " involuntary incarceration? "),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )
    
    citizen = models.CharField(
        verbose_name="3.[Interviewer] Is the prospective participant a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )
    
    community_resident = models.CharField(
        verbose_name=("7.[Participant] In the past 12 months, have you typically spent 3 or"
                      " more nights per month in [name of study community]? [If moved into the"
                      " community in the past 12 months, then since moving in have you typically"
                      " spent more than 3 nights per month in this community] "),
        max_length=17,
        choices=YES_NO_REFUSED,
        validators=[eligible_if_yes, ],
        help_text="if 'NO (or don't want to answer)' STOP participant cannot be enrolled.",
        )
    
    enrolment_reason = models.CharField(
        verbose_name="9. [Interviewer] What is the reason for enrollment of this participant? ",
        max_length=45,
        choices=ENROLMENT_REASON,
        help_text="",
        )
     
    cd4_date = models.DateField(
        verbose_name="10. [Interviewer] Date of the most recent CD4 measurement? ",
        max_length=25,
        help_text="",
        )
     
    cd4_count = models.DecimalField(
        verbose_name="11. [Interviewer] Most recent (within past 3 months) CD4 measurement?",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        )
     
    opportunistic_illness = models.CharField(
        verbose_name=("12. [Interviewer] Does the patient currently have AIDS opportunistic"
                      " illness (refer to SOP for list of eligible conditions)? "),
        max_length=3,
        choices=OPPORTUNISTIC_ILLNESSES,
        help_text="",
        )
     
    diagnosis_date = models.DateField(
        verbose_name="13. [Interviewer] Date of diagnosis of the AIDS opportunistic illness? ",
        max_length=3,
        help_text="",
        )
    
    date_signed = models.DateTimeField(
        verbose_name="14. [Interviewer] Date/ Time study CONSENT signed:",
        max_length=25,
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )

    history = AuditTrail()
    
    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_ceaenrolmentchecklist_change', \
                        args=(self.id,))
    
    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "CEA Enrolment Checklist"
        verbose_name_plural = "CEA Enrolment Checklist"
