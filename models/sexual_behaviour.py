from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_DONT_ANSWER, ALCOHOL_SEX, LASTSEX_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class SexualBehaviour (BaseScheduledVisitModel):
    
    """CS002"""
    
    ever_sex = models.CharField(
        verbose_name=("In your lifetime, have you ever had sex with anyone"
                      " (including your spouse, friends, or someone you have just met)?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    last_year_partners = models.IntegerField(
        verbose_name=("In the past 12 months, how many different people have you had"
                      " sex with?  Please remember to include casual and once-off partners"
                      " (prostitutes and truck drivers) as well as long-term partners"
                      " (spouses, boyfriends/girlfriends)[If you can't recall the exact "
                      "number, please give a best guess]"),
        max_length=2,
        null=True, 
        blank=True,
        help_text="Note:Leave blank if participant does not want to respond. ",
        )

    more_sex = models.CharField(
        verbose_name=("In the past 12 months, did you have sex with somebody"
                      " living outside of the community?"),
        max_length=25,
        null=True, 
        blank=True,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    first_sex = models.IntegerField(
        verbose_name=("How old were you when you had sex for the first time?"
                      " [If you can't recall the exact age, please give a best guess]"),
        max_length=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(64)],
        help_text="Note:leave blank if participant does not want to respond.",
        )

    condom = models.CharField(
        verbose_name=("During the last [most recent] time you had sex, did"
                      " you or your partner use a condom?"),
        max_length=25,
        null=True, 
        blank=True,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    alcohol_sex = models.CharField(
        verbose_name=("During the last [most recent] time you had sex, were"
                      " you or your partner drinking alcohol?"),
        max_length=25,
        null=True, 
        blank=True,
        choices=ALCOHOL_SEX,
        help_text="",
        )

    last_sex = models.CharField(
        verbose_name="When was the last time you had sex?",
        max_length=25,
        choices=LASTSEX_CHOICE,
        null=True,
        blank=True,
        help_text=("Note:Respondent should give the number of days/months/years since last sex"
                   " (e.g. if last sex was last night, then it should be recorded as 1 day). "
                   "Leave blank if participant does not want to respond"),
        )
    last_sex_calc = models.IntegerField(
        verbose_name="Enter the number of days/months/years",
        null=True, 
        blank=True,
        max_length=2,
        )
    
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_sexualbehaviour_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Sexual Behaviour"
        verbose_name_plural = "Sexual Behaviour"
