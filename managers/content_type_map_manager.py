from django.db import models
from django.db.models import F, get_model
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError

class ContentTypeMapManager(models.Manager):

    def sync(self):
    
        """Sync content type map foreignkey with django's ContentType id.
        
        Schema changes might change the key values for records in django's ContentType table.
        Update ContentTypeMap field content_type with the new key.
        
        """
        content_type_maps = super(ContentTypeMapManager, self).exclude(name = F('content_type__name'))
        for content_type_map in content_type_maps:

            if get_model(content_type_map.app_label, content_type_map.model):
                model = get_model(content_type_map.app_label, content_type_map.model)
                if ContentType.objects.filter(app_label=model._meta.app_label, model=model._meta.module_name):
                    content_type = ContentType.objects.get(app_label=model._meta.app_label, model=model._meta.module_name)
                    content_type_map.content_type = content_type
                    content_type_map.save()
            else:    
                content_type_map.delete()
    
    def populate(self):
    
        """Populate ContentTypeMap with django's ContentTypecontent information."""
        
        content_types = ContentType.objects.all()        
        for content_type in content_types:
            if not super(ContentTypeMapManager, self).filter(content_type = content_type):
                if not super(ContentTypeMapManager, self).filter(content_type__name = content_type.name).count() == 1:
                    super(ContentTypeMapManager, self).filter(content_type__name = content_type.name).delete()

                if get_model(content_type.app_label, content_type.model):
                    verbose_name = get_model(content_type.app_label, content_type.model)._meta.verbose_name
                else:
                    verbose_name = content_type.name                    

                try:
                    super(ContentTypeMapManager, self).create(
                        content_type = content_type,
                        app_label = content_type.app_label,
                        name = verbose_name,
                        model = content_type.model,
                        )
                except:
                    pass        
                #except IntegrityError:   
                #    if verbose_name <> 'content type map' and verbose_name <> 'identifier tracker':   
                #        raise TypeError(verbose_name)
                #    pass                  
        
        #content_type_maps = super(ContentTypeMapManager, self).__dict__['model'].objects.all()        
        #for content_type_map in content_type_maps:
        #    if get_model(content_type_map.app_label, content_type_map.model):
        #        verbose_name = get_model(content_type_map.app_label, content_type_map.model)._meta.verbose_name
        #        if not content_type_map.name == verbose_name:
        #            content_type_map.name = verbose_name
        #            content_type_map.save()
