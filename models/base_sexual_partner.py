from django.db import models
from base_scheduled_visit_model import BaseScheduledVisitModel
from bcpp.choices import FIRSTPARTNERLIVE_CHOICE, SEXDAYS_CHOICE, LASTSEX_CHOICE, YES_NO_DONT_ANSWER, YES_NO_UNSURE, FIRSTRELATIONSHIP_CHOICE, FIRSTPARTNERHIV_CHOICE, FIRSTDISCLOSE_CHOICE, FIRSTCONDOMFREQ_CHOICE  


class BaseSexualPartner (BaseScheduledVisitModel):
    
    """CS002"""
    
    firstpartnerlive = models.CharField(
        verbose_name = "1. Over the past 12 months, where has this sexual partner lived to the best of your knowledge?",
        max_length = 15,
        choices = FIRSTPARTNERLIVE_CHOICE,
        help_text="",
        )

    thirdlastsex = models.CharField(
        verbose_name = "2. When was the last [most recent] time you had sex with this person (how long ago)?",
        max_length = 25,
        choices = SEXDAYS_CHOICE,
        help_text="",
        )

    firstfirstsex = models.CharField(
        verbose_name = "3. When was the first time you had sex with this person [how long ago]?",
        max_length = 25,
        choices = LASTSEX_CHOICE,
        help_text="",
        )

    firstsexcurrent = models.CharField(
        verbose_name = "4. Do you expect to have sex with this person again?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    firstrelationship = models.CharField(
        verbose_name = "5. What type of relationship do you have with this person?",
        max_length = 15,
        choices = FIRSTRELATIONSHIP_CHOICE,
        help_text="",
        )

    firstexchange = models.IntegerField(
        verbose_name = "6. To the best of your knowledge, how old is this person?",
        max_length = 2,
        null=True, 
        blank=True,
        help_text="Note: If participant does not want to answer, leave blank. If participant is unable to estimate age, record -4",
        )

    concurrent = models.CharField(
        verbose_name = ("7. Over the past 12 months, during the time you were having a sexual relationship"
                        " with this person, did YOU have sex with other people (including husband/wife)?"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    goods_exchange = models.CharField(
        verbose_name = ("8. Have you received money, transport, food/drink, or other goods in exchange for"
                        " sex from this partner?"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    firstsexfreq= models.IntegerField(
        verbose_name = ("9. During the last 3 months [of your relationship, if it has ended] how many "
                        "times (on average) did you have sex with this partner?"),
        max_length = 2,
        help_text="",
        )

    firstpartnerhiv = models.CharField(
        verbose_name = "Supplemental SH1. What is this partner's HIV status?",
        max_length = 15,
        choices = FIRSTPARTNERHIV_CHOICE,
        help_text="",
        )

    firsthaart = models.CharField(
        verbose_name = "Supplemental SH2. Is this partner taking antiretroviral treatment?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    firstdisclose = models.CharField(
        verbose_name = "Supplemental SH3. Have you told this partner your HIV status?",
        max_length = 15,
        choices = FIRSTDISCLOSE_CHOICE,
        help_text="",
        )

    firstcondomfreq = models.CharField(
        verbose_name = ("Supplemental SH4. When you have [had] sex with this partner, how often "
                        "do you or your partner use a condom?"),
        max_length = 15,
        choices = FIRSTCONDOMFREQ_CHOICE,
        help_text="",
        )

    firstpartnercp = models.CharField(
        verbose_name = ("Supplemental SH5. To the best of your knowledge, did he/she ever have "
                        "other sex partners while you two were having a sexual relationship?"),
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )
    
    class Meta:
        abstract = True
