from base_model import BaseModel
from bhp_base_model.fields import MyUUIDField


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = MyUUIDField(primary_key=True)

    class Meta:
        abstract = True
