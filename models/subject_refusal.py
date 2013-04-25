from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bhp_base_model.validators import date_not_future, date_not_before_study_start
from bhp_common.choices import GENDER, YES_NO_UNSURE
from bcpp.choices import LENGTHRESIDENCE_CHOICE, WHYNOPARTICIPATE_CHOICE, WHYNOHIVTESTING_CHOICE 
from base_member_status_model import BaseMemberStatusModel


class SubjectRefusal (BaseMemberStatusModel):
    
    sex = models.CharField(
        verbose_name="1. [For interviewer] Resident sex?",
        max_length=15,
        choices=GENDER,
        help_text="",
        )
    
    age = models.CharField(
        verbose_name="2. What is your age?",
        max_length=15,
        help_text="Note:If participant does not want to answer, record -8.",
        )
    
    lengthresidence = models.CharField(
        verbose_name="3. How long have your lived in this community?",
        max_length=15,
        choices=LENGTHRESIDENCE_CHOICE,
        help_text="",
        )
    
    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")
    
    whynoparticipate = models.CharField(
        verbose_name="4. What was the main reason you do not want to participate in the study?",
        max_length=15,
        choices=WHYNOPARTICIPATE_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
        )
    whynoparticipate_other = OtherCharField()
    
    subject_refusal_status = models.CharField(
        verbose_name="Refusal status",
        max_length=25,
        help_text=("Change the refusal status from 'refused' to 'no longer refusing' if and"
                   " when the subject changes their mind"),
        default='REFUSED',
        editable=False)
    
    hivtesttoday = models.CharField(
        verbose_name="5. [For interviewer] Did resident complete HIV testing today?",
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="",
        )
    
    whynohivtest = models.CharField(
        verbose_name="6. What was the main reason why you did not want HIV testing as part of today's visit?",
        max_length=15,
        null=True,
        blank=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="if 'Yes or Unsure' END survey",
        )
    
    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        null=True,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment'))
    
    history = AuditTrail()

    def get_absolute_url(self):
        if self.id:
            return reverse('admin:bcpp_subject_subjectrefusal_change', args=(self.id,))
        else:
            return reverse('admin:bcpp_subject_subjectrefusal_add')
    
    def get_registration_datetime(self):
        return self.report_datetime

    def member_status_string(self):
        return 'REFUSED'  
    
    def save(self, *args, **kwargs):
        kwargs['reason'] = 'refuse'
        kwargs['info_source'] = 'subject'
        self.survey = self.household_structure_member.survey
        super(SubjectRefusal, self).save(*args, **kwargs)
     
    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Refusal"
        verbose_name_plural = "Subject Refusal"
        ordering = ['household_structure_member']
