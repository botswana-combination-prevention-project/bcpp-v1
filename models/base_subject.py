from django.db import models
from django.db import IntegrityError
from bhp_common.models import MyBasicUuidModel
from bhp_common.choices import GENDER_UNDETERMINED
from bhp_registration.choices import REGISTRATION_STATUS, SUBJECT_TYPE

class BaseSubject (MyBasicUuidModel):
       
    subject_consent_id = models.CharField(
        max_length=100, 
        null = True,
        blank = True,
        )
       
    # may be null so uniqueness is enforce in save() if not null
    subject_identifier = models.CharField(
        verbose_name = "Subject Identifier",
        max_length=36, 
        # unique = True,
        null = True, 
        blank = True,
        db_index=True,               
        )
    
    first_name = models.CharField(
        max_length=50,
        )
    
    initials = models.CharField(
        max_length=3,
        )                    

    gender = models.CharField(
        verbose_name = "Gender",
        choices = GENDER_UNDETERMINED,
        max_length=1, 
        null = True,
        blank = True,
        )
        
    subject_type = models.CharField(
        max_length = 25,
        #choices=SUBJECT_TYPE,
        )         
    
    screening_datetime=models.DateTimeField(
        null=True,
        blank=True
        )
    
    registration_datetime=models.DateTimeField(        
        null=True,
        blank=True
        )
    
    """ for simplicity, if going straight from screen to rando, 
        update bothe reg date and rando date """
    randomization_datetime=models.DateTimeField(
        null=True,
        blank=True
        )


    registration_status = models.CharField(
        verbose_name = "Registration status",
        max_length = 25,
        #choices=REGISTRATION_STATUS,
        null = True,
        blank = True,
        )
    
    def save(self, *args, **kwargs):
        # for new instances, enforce unique subject_identifier if not null
        if not self.pk and self.subject_identifier:
            if self.__class__.objects.filter(subject_identifier=self.subject_identifier):
                raise IntegrityError, 'Attempt to insert duplicate value for subject_identifier %s when saving %s.' % (self.subject_identifier,self,)
        super(BaseSubject, self).save(*args, **kwargs)

    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.subject_type)
    
    class Meta:
        abstract=True
