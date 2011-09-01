from django.db import models
from django.core.urlresolvers import reverse
from bhp_common.models import MyBasicUuidModel
from bhp_content_type_map.models import ContentTypeMap
from bhp_visit.models import MembershipForm
from bhp_visit.managers import ScheduleGroupManager

    
class ScheduleGroup(MyBasicUuidModel):

    """Model for entry_forms tagged for listing in the visit definition 'tag_for_schedule'."""
    
    group_name = models.CharField(
        max_length=25,
        unique=True,
        )
    
    membership_form = models.ForeignKey(MembershipForm)    
       
    grouping_key = models.CharField(
        max_length = 25,
        null=True,
        blank=True,
        help_text = "may specify a common value to group a number of tagged forms, not required."        
        )        

    objects = ScheduleGroupManager()
    
    def __unicode__(self):
        return unicode(self.group_name)
    
    def get_absolute_url(self):
        return reverse('admin:bhp_visit_schedulegroup_change', args=(self.id,)) 
        
    class Meta:
        ordering = ['group_name']
        app_label = "bhp_visit"
        db_table = 'bhp_form_schedulegroup'
