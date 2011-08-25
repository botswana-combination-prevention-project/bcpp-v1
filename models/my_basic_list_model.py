from django.db import models
from bhp_common.models import MyBasicModel


class MyBasicListModel(MyBasicModel):

    """Basic model for list data used in dropdown and radio widgets having display value and store value pairs."""

    name = models.CharField(
        verbose_name = 'display name', 
        max_length=250, 
        unique=True, 
        help_text = 'This is displayed value, shown to the user (40 characters max.)',
        )

    short_name = models.CharField(
        verbose_name = "store name", 
        max_length=250, 
        unique=True,
        help_text = 'This is the stored value, required',
        )

    display_index = models.IntegerField(
        verbose_name = "display order index",
        #unique=True,
        default = 0,        
        help_text = 'Index to control display order if not alphabetical, not required',
        )

    field_name = models.CharField(
        max_length=25, 
        editable=False, 
        null=True, 
        blank=True,
        help_text = 'Not required',
        )

    version = models.CharField(
        max_length=35, 
        editable=False, 
        default='1.0',
        )

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering=['display_index']


