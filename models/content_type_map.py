from django.db import models
from django.contrib.contenttypes.models import ContentType
from bhp_content_type_map.managers import ContentTypeMapManager
from bhp_base_model.models import BaseModel


class ContentTypeMap(BaseModel):

    content_type = models.ForeignKey(ContentType,
        verbose_name='Link to content type',
        null=True,
        blank=True,
        )

    app_label = models.CharField(
        max_length=50,
        db_index=True,
        )

    name = models.CharField(
        verbose_name='Model verbose_name',
        max_length=50,
        unique=True,
        db_index=True,
        )

    model = models.CharField(
        verbose_name='Model name (module name)',
        max_length=50,
        db_index=True,
        )

    module_name = models.CharField(
        max_length=50,
        null=True,
        )

    objects = ContentTypeMapManager()

    def save(self, *args, **kwargs):
        self.module_name = self.model
        super(ContentTypeMap, self).save(*args, **kwargs)

    def natural_key(self):
        return self.content_type.natural_key()

    def model_class(self):
        if not self.content_type.name.lower() == self.name.lower():
            raise TypeError('ContentTypeMap is not in sync with ContentType for verbose_name %s. Run sync_content_type management command.' % self.name)
        if not self.content_type.model == self.model:
            raise TypeError('ContentTypeMap is not in sync with ContentType for model %s. Run sync_content_type management command.' % self.model)

        return self.content_type.model_class()

    def __unicode__(self):
        return unicode(self.content_type)

    class Meta:
        app_label = 'bhp_content_type_map'
        unique_together = ['app_label', 'model', ]
        ordering = ['name', ]
