from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel


class BaseIdentifierModel(BaseUuidModel):
    """Store identifiers as allocated.

    Will not include identifiers derived from other identifiers, for example, infant and partner
    identifiers are not included in this model.

    To populate for an EDC already in use, for example::
        >>> for rs in RegisteredSubject.objects.filter(subject_type='maternal').order_by('created'):
        >>>    SubjectIdentifier.objects.create(identifier=rs.subject_identifier)
        >>> # or ##############
        >>> for rs in RegisteredSubject.objects.filter(subject_type='subject',
        >>>                                            subject_identifier__isnull=False).order_by('created'):
        >>>    SubjectIdentifier.objects.create(identifier=rs.subject_identifier)

    If there are records in SubjectIdentifier, delete them and reset the autoincrement like this::
        >>> ALTER TABLE `bhp_identifier_subjectidentifier` AUTO_INCREMENT = 1;
    """

    identifier = models.CharField(max_length=36, unique=True, editable=False)
    padding = models.IntegerField(default=4, editable=False)
    sequence_number = models.IntegerField()

    def save(self, *args, **kwargs):
        from bhp_identifier.models import Sequence
        if not 'DEVICE_ID' in dir(settings):
            raise ImproperlyConfigured('Settings attribute DEVICE_ID not found. Add DEVICE_ID =  to your settings.py where DEVICE_ID is a project wide unique integer.')
        sequence = Sequence.objects.create(device_id=settings.DEVICE_ID)
        self.sequence_number = sequence.pk
        super(BaseIdentifierModel, self).save(*args, **kwargs)

    @property
    def sequence(self):
        """Returns a padded sequence segment for the identifier"""
        return str(self.sequence_number).rjust(self.padding, '0')

    def __unicode__(self):
        return self.identifier

    class Meta:
        abstract = True
