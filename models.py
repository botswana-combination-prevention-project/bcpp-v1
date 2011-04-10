from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from bhp_common.models import MyBasicUuidModel
from choices import GENDER_OF_CONSENT, SETTINGS_KEYWORD, MACHINE_TYPE
class BaseStudySpecific (MyBasicUuidModel):

    protocol_number = models.CharField(
        verbose_name = _("BHP Protocol Number"),
        max_length=10,
        unique=True,
        help_text="e.g. BHP056, ...")
    protocol_title = models.CharField(
        verbose_name = _("Protocol Local Title"),
        max_length=100,
        unique=True,        
        help_text=_("Local name for the protocol, e.g. Mashi, Mmabana, ..."))    
    research_title = models.CharField("Protocol Research Title",
        max_length=250,
        unique=True,                
        help_text=_("Protocol title used on the grant"))    
    
    study_start_datetime = models.DateTimeField(
        verbose_name = _("Study Start Date and Time"),
        help_text=_("This is usually the date at which IRB approval was given OR, if later than IRB approval, the date of site activation"),
        )
    minimum_age_of_consent = models.IntegerField(
        verbose_name = _("Minumum age of consent (>=)"),
        )    
    maximum_age_of_consent = models.IntegerField(
        verbose_name = _("Maximum age of consent (<=)"),
        )    
    
    age_at_adult_lower_bound = models.IntegerField(
        verbose_name = _("Lower bound age at adult. Default is 18."),
        default=18,
        help_text = _("At what age is a subject old enough to consent without the presence of a guardian")
        )

    gender_of_consent = models.CharField(
        verbose_name = _("Gender"),
        max_length=3,
        choices=GENDER_OF_CONSENT,
        )

    
    subject_identifier_seed = models.IntegerField(
        verbose_name = _("Subject Identifier Seed (Integer)"),
        default=1000,
        validators = [
            RegexValidator("^[1-9]{1}[0-9]*$", "Ensure first digit is not zero (0)"),
            ],
        help_text="an integer, usually 1000.")

    subject_identifier_prefix = models.CharField(
        verbose_name = _("Subject Identifier prefix"),
        max_length=3,
        unique=True,                
        help_text="Usually the numeric part of protocol_number. E.g. for BHP056 use '056'"
        )

    subject_identifier_modulus = models.IntegerField("Subject Identifier modulus",
        default=7,
        help_text="For the check digit. Use 7 for single digit, 77 for double digit, etc"
        )

    machine_type = models.CharField(
        verbose_name = 'Machine type',
        choices = MACHINE_TYPE,
        max_length=25,
        default='NETBOOK',
        help_text = 'If netbook, other checks are triggered',
        )

    hostname_prefix = models.CharField(
        verbose_name = _("Hostname prefix"),
        max_length=15,
        validators = [
            RegexValidator("^[a-zA-Z]{1,15}$", "Ensure prefix does not contain any spaces or numbers"),
            RegexValidator("^[a-z]{1,15}$", "Ensure prefix is in lowercase"),
            ],
        help_text=_("Refers to the machine hostname. Hostname_prefix+device_id = hostname. To override validation, set hostname_prefix to your hostname and device_id to '0'.")
        )

    device_id = models.IntegerField(
        verbose_name = _("device id"),
        help_text=_("a numeric ID between 10-99 to be part of an identifier that represents the server that allocates an identifier"),
        validators = [
            RegexValidator("^[0]{1}$|^[1-9]{1}[0-9]{1}$", "Ensure value between 10 and 99 (or 0, if override).")
            ]
        )    

    class Meta:
        abstract=True

class StudySpecific (BaseStudySpecific):

    def __unicode__(self):
        return "%s: %s started on %s" % (self.protocol_number, self.protocol_title, self.study_start_datetime)

class StudySite(MyBasicUuidModel):
    
    site_code = models.CharField(max_length=4)        
    
    site_name = models.CharField(max_length=35)    
    
    def __unicode__(self):
        return "%s %s" % (self.site_code, self.site_name)
        
    class Meta:
        unique_together = [('site_code', 'site_name')]    
        
