from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_crypto.fields import EncryptedCharField
from bcpp.choices import COMMUNITIES
from bcpp_household.managers import WardManager


class Ward(BaseUuidModel):
    village_name = EncryptedCharField(
        choices=COMMUNITIES,
     )
     
    ward_name = EncryptedCharField(
        max_length=30,
        db_index=True,
     )

    objects = WardManager()

    def __unicode__(self):
        return "{0}-{1}".format(self.village_name, self.ward_name)
    
    class Meta:
        app_label = "bcpp_household"
        verbose_name = "Wards"
