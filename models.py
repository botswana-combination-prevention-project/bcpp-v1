from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_basic_models.models import MyBasicModel

class StudySpecific (MyBasicModel):
    protocol_number = models.CharField("Protocol number",
        max_length=10,
        unique=True,
        help_text="e.g. BHP056, ...")
    protocol_title = models.CharField("Protocol Title",
        max_length=100,
        help_text="Local name for the protocol, e.g. Mashi, Mmabana, ...")    
    research_title = models.CharField("Protocol Title",
        max_length=250,
        help_text="Protocol title used on the grant")    
    study_start_datetime = models.DateTimeField("Study Start Date and Time",
        help_text="This is usually the date at which IRB approval was given OR, if later than IRB approval, the date of site activation"
        )
    subject_identifier_seed = models.IntegerField("Subject Identifier Seed (Integer)",
        help_text="an integer, usually 1000")
    subject_identifier_prefix = models.CharField("Subject Identifier prefix",
        max_length=3,
        blank=True,
        help_text="Usually the numeric part of protocol_number. E.g. for BHP056 use '056'"
        )
    subject_identifier_modulus = models.IntegerField("Subject Identifier modulus",
        help_text="For the check digit. Use 7 for single digit, 77 for double digit, etc"
        )

    device_id = models.IntegerField("device id",
        help_text="a numeric ID between 10-99 to be part of an identifier that represents the server that allocates an identifier",
        validators = [
            MinValueValidator(10),
            MaxValueValidator(99),
            ]
    )    

    def __unicode__(self):
        return "%s: %s started on %s" % (self.protocol_number, self.protocol_title, self.study_start_datetime)
