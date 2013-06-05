from django.db import models
from django.db.models import Max
from bhp_base_model.models import BaseModel


class Section(BaseModel):

    name = models.CharField(max_length=25)
    display_name = models.CharField(max_length=25, null=True, blank=True)
    display_index = models.IntegerField(null=True, blank=True)
    display = models.BooleanField(default=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.display_name:
            self.display_name = '{0}{1}'.format(self.name[0].upper(), self.name[1:])
        if not self.display_index:
            aggr = self.__class__.objects.values('display_index').all().annotate(Max('display_index'))
            self.display_index = int(aggr[0].get('display_index__max', 0)) + 10
        super(Section, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'bhp_section'
