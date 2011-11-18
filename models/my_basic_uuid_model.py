from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.db.models import get_model
from bhp_common.models import MyBasicModel
from bhp_common.fields import MyUUIDField


class MyBasicUuidModel(MyBasicModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """
    
    id = MyUUIDField(primary_key=True)

    def is_serialized(self, serialize=False):

        if 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
            if settings.ALLOW_MODEL_SERIALIZATION:
                return serialize
        return False
        
    def save(self, *args, **kwargs):

        super(MyBasicUuidModel, self).save(*args, **kwargs)
        
        if self.pk and self.is_serialized() and not self._meta.proxy:
            # serialize to file
            # no need to serialize upon 'proxy model' save() as this will get called from the 'model' save()
            #fname = '%s%s-%s.json' % (settings.MEDIA_ROOT, datetime.today().strftime('%Y%m%d%H%M%S%f'), str(self.pk),) 
            #fd = open(fname, "w")
            #serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), stream=fd)
            #fd.close()
            transaction = get_model('bhp_sync', 'transaction')
            json = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), )            
            transaction.objects.create(
                tx_name = self._meta.object_name,
                tx_pk = self.pk,
                tx = json,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                )
            
    
    class Meta:
        abstract = True
