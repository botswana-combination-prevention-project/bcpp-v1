from django.db import models
from django.core.urlresolvers import reverse
from bhp_common.models import MyBasicUuidModel
from bhp_common.models import ContentTypeMap
from bhp_visit.choices import SUBJECT_TYPE

class ScheduleGroupManager(models.Manager):

    def get_membership_forms_for(self, registered_subject):
        """ Return dict of keyed and unkeyed schedule group membership forms for registered_subject"""
        """
rs=RegisteredSubject.objects.all()[0]
s = ScheduleGroup.objects.get_membership_forms(rs)
        """
        grouping_keys = []
        keyed_membership_forms = {}
        #get KEYED schedule group membership forms
        for schedule_group in super(ScheduleGroupManager, self).all():
            membership_form_model = ContentTypeMap.objects.get(name = schedule_group.membership_form).model_class()
            if 'registered_subject' in [f.name for f in membership_form_model._meta.fields]:
                if membership_form_model.objects.filter(registered_subject = registered_subject):
                    # need to collect grouping key for schedule groups that have more than one membership form
                    grouping_keys.append(schedule_group.grouping_key)
                    # add keyed 
                    keyed_membership_forms[schedule_group.membership_form.name] = membership_form_model.objects.get(registered_subject = registered_subject) 

        #get UNKEYED schedule group membership forms            
        # ...use the grouping key to eliminate membership forms related to a KEYED form from above
        unkeyed_membership_forms = [schedule_group.membership_form for schedule_group in super(ScheduleGroupManager, self).all() 
                                        if schedule_group.grouping_key not in grouping_keys]

        return {'keyed': keyed_membership_forms, 'unkeyed':unkeyed_membership_forms}
    
class ScheduleGroup(MyBasicUuidModel):

    """Model for entry_forms tagged for listing in the visit definition 'tag_for_schedule'."""
    
    group_name = models.CharField(
        max_length=25,
        unique=True,
        )
    
    membership_form = models.ForeignKey(ContentTypeMap)
        
    subject_type = models.CharField(
        max_length = 25,
        choices = SUBJECT_TYPE,
        )       

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
        app_label = 'bhp_visit'         
