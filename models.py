from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_basic_models.models import MyBasicModel

class Configuration (MyBasicModel):
    protocol_number = models.CharField("Protocol number",
        max_length=10,
        unique=True)
    protocol_title = models.CharField("Protocol Title",
        max_length=100)    
    study_start_datetime = models.DateTimeField("Study Start Date and Time")
    subject_identifier_seed = models.IntegerField("Subject Identifier Seed (Integer)")
    subject_identifier_prefix = models.CharField("Subject Identifier prefix",
        max_length=3
        )
    device_id = models.IntegerField("device id",
        validators = [
            MinValueValidator(10),
            MaxValueValidator(99),
            ]
    )    

    def __unicode__(self):
        return "%s: %s started on %s" % (self.protocol_number, self.protocol_title, self.study_start_datetime)
