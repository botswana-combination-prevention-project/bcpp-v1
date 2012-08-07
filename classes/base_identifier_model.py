from django.db import models
from bhp_base_model.classes import BaseModel


class BaseIdentifierModel(BaseModel):
    """Store identifiers as allocated and use the pk as a unique sequence for the new identifier.

    Will not include identifiers derived from other identifiers, for example, infant and partner
    identifiers are not included in this model.

    To populate for an EDC already in use, for example:

        >>>for rs in RegisteredSubject.objects.filter(subject_type='maternal').order_by('created'):
        >>>    SubjectIdentifier.objects.create(identifier=rs.subject_identifier, seed='1000')

    If there are records in SubjectIdentifier, delete them and reset the autoincrement like this:

        >>> ALTER TABLE `bhp_identifier_subjectidentifier` AUTO_INCREMENT = 1;
    """

    identifier = models.CharField(max_length=25, unique=True)
    seed = models.IntegerField()
    padding = models.IntegerField(default=4)

    @property
    def sequence(self):
        """Returns a padded sequence segment of the identifier based on the auto-increment
        integer primary key"""
        return str(self.pk).rjust(self.padding, '0')

    def __unicode__(self):
        return self.identifier

    class Meta:
        abstract = True
