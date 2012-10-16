from django.db import models
from django.core.urlresolvers import reverse
from bhp_content_type_map.models import ContentTypeMap
from bhp_base_model.classes import BaseUuidModel
from bhp_visit.managers import MembershipFormManager


class MembershipForm(BaseUuidModel):

    """Model to list forms to be linked to a ShceduleGroup as "registration" forms to that group"""

    content_type_map = models.OneToOneField(ContentTypeMap, related_name='+')
    category = models.CharField(
        max_length=25,
        default='subject',
        null=True,
        help_text='In lowercase, this should be a valid subject type (as in registered_subject).')
    visible = models.BooleanField(
        default=True,
        help_text='If not visible on the dashboard, you have to write code to populate it yourself.')
    objects = MembershipFormManager()

    def natural_key(self):
        return self.content_type_map.natural_key()

    def get_absolute_url(self):
        return reverse('admin:bhp_visit_membershipform_change', args=(self.id,))

    def __unicode__(self):
        return self.content_type_map.name

    class Meta:
        app_label = "bhp_visit"
