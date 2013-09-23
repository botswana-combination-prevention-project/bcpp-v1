from base_model import BaseModel
from django_extensions.db.fields import UUIDField


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = UUIDField(primary_key=True)

    class Meta:
        abstract = True
