from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator, MinLengthValidator
from bhp_base_model.models import BaseUuidModel
from bhp_variables.choices import GENDER_OF_CONSENT, MACHINE_TYPE
from bhp_variables.managers import StudySpecificManager


class BaseStudySpecific (BaseUuidModel):

    protocol_number = models.CharField(
        verbose_name=_("BHP Protocol Number"),
        max_length=10,
        unique=True,
        help_text="e.g. BHP041, BHP056, ..."
        )

    protocol_code = models.CharField(
        verbose_name=_("BHP Protocol Code"),
        max_length=3,
        validators=[MinLengthValidator(3), ],
        unique=True,
        help_text="Three digit code mostly for identifiers. e.g. 041, 056, ..."
        )

    protocol_title = models.CharField(
        verbose_name=_("Protocol Local Title"),
        max_length=100,
        unique=True,
        help_text=_("Local name for the protocol, e.g. Mashi, Mmabana, ...")
        )

    research_title = models.CharField("Protocol Research Title",
        max_length=250,
        unique=True,
        help_text=_("Protocol title used on the grant")
        )

    study_start_datetime = models.DateTimeField(
        verbose_name=_("Study Start Date and Time"),
        help_text=_("This is usually the date at which IRB approval was given OR, if later than IRB approval, the date of site activation"),
        )

    minimum_age_of_consent = models.IntegerField(
        verbose_name=_("Minumum age of consent (>=)"),
        )

    maximum_age_of_consent = models.IntegerField(
        verbose_name=_("Maximum age of consent (<=)"),
        )

    age_at_adult_lower_bound = models.IntegerField(
        verbose_name=_("Lower bound age at adult. Default is 18."),
        default=18,
        help_text=_("At what age is a subject old enough to consent without the presence of a guardian")
        )

    gender_of_consent = models.CharField(
        verbose_name=_("Gender"),
        max_length=3,
        choices=GENDER_OF_CONSENT,
        )

    subject_identifier_seed = models.IntegerField(
        verbose_name=_("Subject Identifier Seed (Integer)"),
        default=1000,
        validators=[
            RegexValidator("^[1-9]{1}[0-9]*$", "Ensure first digit is not zero (0)"),
            ],
        help_text="an integer, usually 1000."
        )

    subject_identifier_prefix = models.CharField(
        verbose_name=_("Subject Identifier prefix"),
        max_length=3,
        unique=True,
        help_text="Usually the numeric part of protocol_number. E.g. for BHP056 use '056'"
        )

    subject_identifier_modulus = models.IntegerField("Subject Identifier modulus",
        default=7,
        help_text="For the check digit. Use 7 for single digit, 77 for double digit, etc"
        )

    subject_type = models.CharField(
        verbose_name='Subject type',
        max_length=100,
        validators=[RegexValidator('(^[a-z]+$|^[a-z]+\,\ [a-z]+$)+', "use lower case comma delimited. e.g. <subject_type>, <subject_type>, ...")],
        default='subject',
        help_text='in lower case separate by <comma><space> (e.g. <subject_type>, <subject_type>, ...)',
        )

    machine_type = models.CharField(
        verbose_name='Machine type',
        choices=MACHINE_TYPE,
        max_length=25,
        default='',
        help_text='If netbook, other checks are triggered',
        )

    hostname_prefix = models.CharField(
        verbose_name=_("Hostname prefix"),
        max_length=15,
        validators=[
            RegexValidator("^[a-z0-9\.]{1,15}$", "Ensure prefix contains only numbers and lowercase letters and does not contain any spaces"),
            ],
        help_text=_("Refers to the machine hostname. Hostname_prefix+device_id = hostname. To override validation, set hostname_prefix to your hostname and device_id to '0'.")
        )

    device_id = models.IntegerField(
        verbose_name=_("device id"),
        help_text=_("a numeric ID between 10-99 to be part of an identifier that represents the server that allocates an identifier"),
        validators=[
            RegexValidator("^[0]{1}$|^[1-9]{1}[0-9]{1}$", "Ensure value between 10 and 99 (or 0, if override).")
            ]
        )

    objects = StudySpecificManager()

    class Meta:
        abstract = True


class StudySpecific (BaseStudySpecific):

    def protocol_prefix(self):
        return self.protocol_code

    def __unicode__(self):
        return "%s: %s started on %s" % (self.protocol_number, self.protocol_title, self.study_start_datetime)

    class Meta:
        app_label = 'bhp_variables'
