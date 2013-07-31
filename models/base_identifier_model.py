from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from bhp_sync.models import BaseSyncUuidModel
from base_sequence import BaseSequence
from bhp_identifier.managers import IdentifierManager


class BaseIdentifierModel(BaseSyncUuidModel):
    """Store identifiers as allocated.
    """

    identifier = models.CharField(max_length=36, unique=True, editable=False)
    padding = models.IntegerField(default=4, editable=False)
    sequence_number = models.IntegerField()
    device_id = models.IntegerField(default=0)
    is_derived = models.BooleanField(default=False)
    sequence_app_label = models.CharField(max_length=50, editable=False, default='bhp_identifier')
    sequence_model_name = models.CharField(max_length=50, editable=False, default='sequence')

    def save(self, *args, **kwargs):
        if not 'DEVICE_ID' in dir(settings):
            raise ImproperlyConfigured('Settings attribute DEVICE_ID not found. Add DEVICE_ID = to your settings.py where DEVICE_ID is a project wide unique integer.')
        if not self.id:
            self.device_id = settings.DEVICE_ID
            if self.is_derived == True:
                self.sequence_number = 0
            else:
                if not self.sequence_app_label or not self.sequence_model_name:
                    raise AttributeError('Attributes sequence_app_label and sequence_model_name may not be None. These are needed to \'get_model\' the Sequence table. Got {0}'.format((self.sequence_app_label, self.sequence_model_name)))
                Sequence = models.get_model(self.sequence_app_label, self.sequence_model_name)
                if not issubclass(Sequence, BaseSequence):
                    raise TypeError('Expected Sequence model to be a subclass of BaseSequence. Using {0}. Got {1}'.format((self.sequence_app_label, self.sequence_model_name), Sequence))
                sequence = Sequence.objects.using(kwargs.get('using', None)).create(device_id=settings.DEVICE_ID)
                self.sequence_number = sequence.pk
        if self.identifier == None:
            raise AttributeError('IdentifierModel attribute \'identifier\' cannot be None. Set as a unique uuid or a unique formatted identifier.')
        if self.sequence_number == None:
            raise AttributeError('IdentifierModel attribute \'sequence\' cannot be None.')
        super(BaseIdentifierModel, self).save(*args, **kwargs)

    @property
    def formatted_sequence(self):
        """Returns a padded sequence segment for the identifier"""
        if self.is_derived == True:
            return ''
        return str(self.sequence_number).rjust(self.padding, '0')

    objects = IdentifierManager()
    
    def natural_key(self):
        return (self.identifier, self.device_id, )
    
    def __unicode__(self):
        return self.identifier

    class Meta:
        abstract = True
