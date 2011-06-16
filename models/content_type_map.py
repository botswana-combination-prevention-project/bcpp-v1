from django.db import models
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from base_models import MyBasicModel

class ContentTypeMapManager(models.Manager):

    def sync(self):
    
        """Sync content type map foreignkey with django's ContentType id.
        
        Schema changes might change the key values for records in django's ContentType table.
        Update ContentTypeMap field content_type with the new key.
        
        """
        content_type_maps = super(ContentTypeMapManager, self).exclude(name = F('content_type__name'))
        for content_type_map in content_type_maps:
            try:
                content_type = ContentType.objects.get(name = content_type_map.name)
                content_type_map.content_type = content_type
                content_type_map.save()
            except:    
                content_type_map.delete()
    
    def populate(self):
    
        """Populate ContentTypeMap with django's ContentTypecontent information."""
        
        content_types = ContentType.objects.all()        
        for content_type in content_types:
            if not super(ContentTypeMapManager, self).filter(content_type = content_type):
                super(ContentTypeMapManager, self).create(
                    content_type = content_type,
                    app_label = content_type.app_label,
                    name = content_type.name,
                    model = content_type.model,
                    )

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
    
    objects =  ContentTypeMapManager()  
    
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

