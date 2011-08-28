from bhp_common.models import MyBasicModel
from bhp_common.fields import MyUUIDField

class MyBasicUuidModel(MyBasicModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """
    
    id = MyUUIDField(primary_key=True)



    class Meta:
        abstract = True
