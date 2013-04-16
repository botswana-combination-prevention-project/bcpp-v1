from django.db import models
from django.core.urlresolvers import reverse
from bhp_base_model.fields import OtherCharField
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO_REFUSED
from bcpp_subject.choices import EMPLOYMENT_INFO, OCCUPATION, MONTHLY_INCOME, SALARY, HOUSEHOLD_INCOME, OTHER_OCCUPATION, GRANT_TYPE
from base_scheduled_visit_model import BaseScheduledVisitModel
from my_base_uuid_model import MyBaseUuidModel


class LabourMarketWages (BaseScheduledVisitModel):
    
    """CE001"""
    
    employed = models.CharField(
        verbose_name="6. Are you currently employed? ",
        max_length=40,
        choices=EMPLOYMENT_INFO,
        help_text="if 'NO or Don't want to answer' go to question Q12",
        )
    occupation = models.CharField(
        verbose_name="7. What is your occupation?",
        max_length=40,
        choices=OCCUPATION,
        null=True,
        blank=True,
        help_text="",
        )
    occupation_other = OtherCharField()
    
    job_description_change = models.IntegerField(
        verbose_name=("8. In the past 3 months, how many times have you changed your job? "
                      "For example, changed your type of work or your employer. "),
        max_length=2,
        null=True,
        blank=True,
        help_text="Note: Enter number of times. If participant does not want to answer, leave blank",
        )
    
    days_worked = models.IntegerField(
        verbose_name="9. In the past month, how many days did you work?. ",
        max_length=2,
        null=True,
        blank=True,
        help_text="Note: Enter number of times. If participant does not want to answer, leave blank",
        )
    monthly_income = models.CharField(
        verbose_name="10. In the past month, what was your income? ",
        max_length=25,
        choices=MONTHLY_INCOME,
        null=True,
        blank=True,
        help_text="",
        )
    salary_payment = models.CharField(
        verbose_name="11. How were you paid for your work? ",
        max_length=20,
        choices=SALARY,
        null=True,
        blank=True,
        help_text="",
        )
    household_income = models.CharField(
        verbose_name="12. In the past month, what was the income of your household? ",
        max_length=25,
        choices=HOUSEHOLD_INCOME,
        help_text="",
        )
    other_occupation = models.CharField(
        verbose_name="13. If you are not currently doing anything to earn money, then are you: ",
        max_length=45,
        choices=OTHER_OCCUPATION,
        help_text="",
        )
    other_occupation_other = OtherCharField()
    
    govt_grant = models.CharField(
        verbose_name="14. Do you receive any government grant for yourself or on behalf of someone else? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
#     = models.CharField(
#         verbose_name="15. How many of each type of grant do you receive? ",
#         max_length=,
#         choices=,
#         help_text="",
#         )
    nights_out = models.IntegerField(
        verbose_name="16. In the past month, how many nights did you spend away from home?. ",
        max_length=2, 
        null=True,
        blank=True,
        help_text="Note: Enter number of nights. If participant does not want to answer, leave blank",
        )
    weeks_out = models.CharField(
        verbose_name="17. In the last 12 months, have you spent more than 2 weeks away? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    days_not_worked = models.IntegerField(
        verbose_name=("18. How many days have you been prevented from working because of sickness"
                      " or visits to seek healthcare in the last 3 months. "),
        max_length=2,
        null=True,
        blank=True,
        help_text="Note: Enter number of days including zero. If participant does not want to answer,leave blank",
        )
    days_inactivite = models.IntegerField(
        verbose_name=("19. How many days have you been prevented by illness from doing the things"
                      " you normally do (studying, housework etc.) because of sickness or visits to"
                      " seek healthcare in the last 3 months? "),
        max_length=2,
        null=True,
        blank=True,
        help_text="Note: Enter number of days including zero. If participant does not want to answer, leave blank",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_labourmarketwages_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Labour Market & Lost Wages"
        verbose_name_plural = "Labour Market & Lost Wages"


class GrantType(MyBaseUuidModel):
    
    grant_number = models.IntegerField(
        verbose_name="How many of each type of grant do you receive?",
        max_length=2,
        )
    grant_type = models.CharField(
        verbose_name="Grant name",
        choices=GRANT_TYPE,
        max_length=34,
        )
    other_grant = OtherCharField()
    
    class Meta:
        abstract = True


class Grant(GrantType):
    
    labour_market_wages = models.ForeignKey(LabourMarketWages)
    
    history = AuditTrail()
    
    class Meta: 
        app_label = 'bcpp_subject'
        verbose_name = "Grants"
        verbose_name_plural = "Grants"
    