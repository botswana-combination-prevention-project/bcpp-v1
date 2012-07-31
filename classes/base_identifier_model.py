from django.db import models
from bhp_base_model.classes import BaseModel


class BaseIdentifierModel(BaseModel):
    """Store identifiers as allocated and use the pk as a unique sequence for the new identifier.

    Will not include identifiers derived from other identifiers, for example, infant and partner
    identifiers are not included in this model."""

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
