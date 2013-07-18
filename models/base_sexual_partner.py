from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from base_scheduled_visit_model import BaseScheduledVisitModel
from bcpp_list.models import PartnerResidency
from bcpp.choices import SEXDAYS_CHOICE, LASTSEX_CHOICE, YES_NO_DONT_ANSWER, YES_NO_UNSURE, FIRSTRELATIONSHIP_CHOICE, FIRSTPARTNERHIV_CHOICE, FIRSTDISCLOSE_CHOICE, FIRSTCONDOMFREQ_CHOICE


class BaseSexualPartner (BaseScheduledVisitModel):

    """CS002"""

    first_partner_live = models.ManyToManyField(PartnerResidency,
        verbose_name=("Over the past 12 months, where has this sexual partner"
                      " lived to the best of your knowledge?"),
        help_text="",
        )

    third_last_sex = models.CharField(
        verbose_name=("When was the last [most recent] time you had sex with"
                      " this person (how long ago)?"),
        max_length=25,
        choices=SEXDAYS_CHOICE,
        help_text="",
        )
    third_last_sex_calc = models.IntegerField(
        verbose_name="Give the number of days/ months since last had sex.",
        max_length=2,
        help_text="e.g. if last sex was last night, then it should be recorded as 1 day",
        )

    first_first_sex = models.CharField(
        verbose_name="When was the first time you had sex with this person [how long ago]?",
        max_length=25,
        choices=LASTSEX_CHOICE,
        help_text="",
        )
    first_first_sex_calc = models.IntegerField(
        verbose_name="Give the number of days/ months since first had sex.",
        max_length=2,
        help_text="e.g. if first sex was last night, then it should be recorded as 1 day",
        )

    first_sex_current = models.CharField(
        verbose_name="Do you expect to have sex with this person again?",
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    first_relationship = models.CharField(
        verbose_name="What type of relationship do you have with this person?",
        max_length=40,
        choices=FIRSTRELATIONSHIP_CHOICE,
        help_text="",
        )

    first_exchange = models.IntegerField(
        verbose_name="To the best of your knowledge, how old is this person?",
        max_length=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(64)],
        help_text=("Note: If participant does not want to answer, leave blank."
                   " If participant is unable to estimate age, record -4"),
        )

    concurrent = models.CharField(
        verbose_name=("Over the past 12 months, during the time you were having a sexual relationship"
                        " with this person, did YOU have sex with other people (including husband/wife)?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    goods_exchange = models.CharField(
        verbose_name=("Have you received money, transport, food/drink, or other goods in exchange for"
                        " sex from this partner?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    first_sex_freq = models.IntegerField(
        verbose_name=("During the last 3 months [of your relationship, if it has ended] how many "
                        "times did you have sex with this partner?"),
        max_length=2,
        help_text="",
        )

    first_partner_hiv = models.CharField(
        verbose_name="What is this partner's HIV status?",
        max_length=25,
        choices=FIRSTPARTNERHIV_CHOICE,
        null=True,
        help_text="",
        )
    
    partner_hiv_test = models.CharField(
        verbose_name="Has your partner been tested for HIV in last 12 months",
        choices=YES_NO_UNSURE,
        max_length=15,
        help_text="",
        )

    first_haart = models.CharField(
        verbose_name="Is this partner taking antiretroviral treatment?",
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        blank=True,
        help_text="supplemental",
        )

    first_disclose = models.CharField(
        verbose_name="Have you told this partner your HIV status?",
        max_length=30,
        choices=FIRSTDISCLOSE_CHOICE,
        null=True,
        help_text="supplemental",
        )

    first_condom_freq = models.CharField(
        verbose_name=("When you have [had] sex with this partner, how often "
                        "do you or your partner use a condom?"),
        max_length=25,
        choices=FIRSTCONDOMFREQ_CHOICE,
        null=True,
        help_text="supplemental",
        )

    first_partner_cp = models.CharField(
        verbose_name=("To the best of your knowledge, did he/she ever have "
                        "other sex partners while you two were having a sexual relationship?"),
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="supplemental",
        )

    class Meta:
        abstract = True
