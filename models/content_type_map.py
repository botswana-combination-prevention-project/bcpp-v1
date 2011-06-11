from django.db import models
from django.db.models import F
from django.contrib.contenttypes.models import ContentType

class ContentTypeMapManager(models.Manager):

    def sync(self):
    
        content_type_maps = super(ContentTypeMapManager, self).exclude(name = F('content_type__name'))

        for content_type_map in content_type_maps:
            content_type = ContentType.objects.get(name = content_type_map.name)
            content_type_map.content_type = content_type
            content_type_map.save()

class ContentTypeMap(MyBasicModel):

    content_type = models.ForeignKey(ContentType,
        verbose_name = 'Link to content type'
        )

    app_label = models.CharField(
        max_length = 50,
        )
    
    name = models.CharField(
        max_length = 50,
        unique = True,
        )
        
    model = models.CharField(
        max_length = 50,
        unique = True,        
        )
    
    def model_class(self):

        if not self.content_type.name == self.name:
            raise TypeError('ContentTypeMap is not in sync with ContentType for verbose_name %s' % self.name) 
        if not self.content_type.model == self.model:
            raise TypeError('ContentTypeMap is not in sync with ContentType for model %s' % self.model)
        
        return self.content_type.model_class()
    
    def __unicode__(self):
        return unicode(self.content_type)        

    class Meta:
        app_label = 'bhp_common'

