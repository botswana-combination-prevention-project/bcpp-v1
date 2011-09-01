from django.db import models
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from bhp_content_type_map.managers import ContentTypeMapManager
from bhp_common.models import MyBasicModel

class ContentTypeMap(MyBasicModel):

    content_type = models.ForeignKey(ContentType,
        verbose_name = 'Link to content type',
        null = True,
        blank=True,
        )

    app_label = models.CharField(
        max_length = 50,
        )
    
    name = models.CharField(
        verbose_name = 'Model verbose_name',
        max_length = 50,
        unique = True,
        )
        
    model = models.CharField(
        verbose_name = 'Model name (module name)',
        max_length = 50,
        )
    
    objects =  ContentTypeMapManager()  
    
    def model_class(self):

        """
        if not self.content_type.name == self.name:
            c = ContentTypeMapManager()
            c.sync()
        if not self.content_type.model == self.model:
            c = ContentTypeMapManager()
            c.sync()
        """                    
        if not self.content_type.name == self.name:
            raise TypeError('ContentTypeMap is not in sync with ContentType for verbose_name %s' % self.name) 
        if not self.content_type.model == self.model:
            raise TypeError('ContentTypeMap is not in sync with ContentType for model %s' % self.model)
        
        return self.content_type.model_class()
    
    def __unicode__(self):
        return unicode(self.content_type)        

    class Meta:
        app_label = 'bhp_content_type_map'
        db_table = 'bhp_common_contenttypemap'
        unique_together = ['app_label', 'model',]

