from django.db import models
from base_scheduled_visit_model import BaseScheduledVisitModel
from bhp_base_model.fields import OtherCharField
from bhp_common.choices import GENDER, YES_NO_REFUSED, POS_NEG_UNKNOWN, YES_NO_DONT_KNOW
from bcpp_subject.choices import RELATIONSHIP_TYPE, MAIN_PARTNER_RESIDENCY, SEX_REGULARITY, INTERCOURSE_TYPE


class DetailedSexualHistory (BaseScheduledVisitModel):
    
    """CS003"""
    
    rel_type = models.CharField(
        verbose_name="1.  What type of relationship do you have with this person? ",
        max_length=37,
        choices=RELATIONSHIP_TYPE,
        help_text="",
        )
    rel_type_other = OtherCharField()
    
    partner_residency = models.CharField(
        verbose_name="2. To the best of your knowledge, where does you main sexual partner live? ",
        max_length=25,
        choices=MAIN_PARTNER_RESIDENCY,
        help_text="",
        )
    partner_age = models.IntegerField(
        verbose_name="3. How old is this sexual partner?",
        max_length=2,
        help_text="If you don't know for sure, please give a best guess",
        )
    partner_gender = models.CharField(
        verbose_name="4. Is this partner male or female? ",
        max_length=6,
        choices=GENDER,
        help_text="",
        )
    last_sex_contact = models.DateField(
        verbose_name="5. When was the last (most recent) time you had sex with this person (how long ago)? ",
        max_length=25,
        choices=MAIN_PARTNER_RESIDENCY,
        help_text="You can give either a date or the number of days/months/years since last sex. Interviewer, convert to days and record",
        )
    last_sex_contact_other = OtherCharField(
        verbose_name="Record number of days converted to.",
        )
    first_sex_contact = models.DateField(
        verbose_name="6.When was the first time you had sex with this person (how long ago)? ",
        max_length=25,
        choices=MAIN_PARTNER_RESIDENCY,
        help_text="You can give either a date or the number of days/months/years since last sex. Interviewer, convert to days and record",
        )
    first_sex_contact_other = OtherCharField(
        verbose_name="Record number of days converted to.",
        )
    regular_sex = models.IntegerField(
        verbose_name=("7.During the last 3 months (of your relationship if it has ended) how"
                      " many times a month (on average) did you have sex?"),
        max_length=2,
        help_text="",
        )
    having_sex = models.CharField(
        verbose_name="8. Are you still having sex with this person? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    having_sex_reg = models.CharField(
        verbose_name="9. Are you still having sex with this person? ",
        max_length=17,
        choices=SEX_REGULARITY,
        help_text="",
        )
    alcohol_before_sex = models.CharField(
        verbose_name="10. Last time you had sex with this partner, did you drink alcohol before sex? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    partner_status = models.CharField(
        verbose_name="11. Have you learned this partner's HIV status? ",
        max_length=8,
        choices=POS_NEG_UNKNOWN,
        help_text=" if 'HIV-negative or Don't know' go to question XX",
        )
    partner_arv = models.CharField(
        verbose_name="12. Is this partner taking antiretroviral treatment?  ",
        max_length=8,
        null=True,
        blank=True,
        choices=YES_NO_DONT_KNOW,
        help_text="",
        )
    status_disclosure = models.CharField(
        verbose_name="13.Have you disclosed your HIV status to this partner? ",
        max_length=8,
        null=True,
        blank=True,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    multiple_partners = models.CharField(
        verbose_name=("14. To the best of your knowledge, did he/she ever have other"
                      " sex partners while you two were having a sexual relationship?"),
        max_length=8,
        null=True,
        blank=True,
        choices=YES_NO_DONT_KNOW,
        help_text="",
        )
    intercourse_type = models.CharField(
        verbose_name="15. Can you tell me what type of sex you had with this sex partner?  ",
        max_length=8,
        null=True,
        blank=True,
        choices=INTERCOURSE_TYPE,
        help_text=("Remember: Vaginal sex is when a man puts his penis in the vagina of a woman."
                   " Anal sex is when a man puts his penis in the rectum of a man or a woman."),
        )

    class Meta:
        abstract = True
