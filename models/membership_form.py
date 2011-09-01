from django.db import models
from django.core.urlresolvers import reverse
from bhp_common.choices import YES_NO
from bhp_content_type_map.models import ContentTypeMap
from bhp_common.models import MyBasicUuidModel

class MembershipForm(MyBasicUuidModel):

    """Model to list forms to be linked to a ShceduleGroup as "registration" forms to that group"""
    
    content_type_map = models.ForeignKey(ContentTypeMap, related_name='+')
    
    category = models.CharField(
        max_length = 25,
        default = 'subject',
        null = True,
        help_text = 'In lowercase, this should be a valid subject type (as in registered_subject).'
        )       
    
    hide_from_dashboard = models.BooleanField(
        default = False,
        help_text = 'If you hide this form from the dashboard, you must write code to populate it yourself.',
        )
    
    def get_absolute_url(self):
        return reverse('admin:bhp_visit_membershipform_change', args=(self.id,))

    def __unicode__(self):        
        return self.content_type_map.name
    
    class Meta:
        app_label = "bhp_visit"
        db_table = 'bhp_form_membershipform'

