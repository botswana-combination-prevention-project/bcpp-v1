from django.db import models
from django.core.urlresolvers import reverse
from bhp_base_model.models import BaseModel


class ModelHelpText(BaseModel):

    help_text = models.TextField(
        max_length=500,
        null=True,
        blank=True)
    additional_comment = models.TextField(
        max_length=500,
        null=True,
        blank=True)
    trans_assistance = models.TextField(
        max_length=500,
        null=True,
        blank=True)
    status = models.CharField(
        max_length=35,
        choices=(('active', 'Active'), ('inactive', 'Inactive')),
        default='Active')
    app_label = models.CharField(max_length=50)
    module_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=50)
    objects = models.Manager()

    def url(self):
        url = reverse('admin:{app_label}_{module_name}_add'.format(app_label=self.app_label, module_name=self.module_name))
        ret = """<a href="{url}" />review form</a>""".format(url=url)
        return ret
    url.allow_tags = True

    class Meta:
        app_label = "bhp_data_manager"
