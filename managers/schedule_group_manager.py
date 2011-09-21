from django.db import models
from django.db.models import Q


class ScheduleGroupManager(models.Manager):

    def get_membership_forms_for(self, **kwargs):

        """ Return dict of keyed and unkeyed schedule group membership forms for registered_subject
        
        Specify the registered_subject and the membership_form_category. Include forms
        of the specified membership_form__category AND those that have no category (null) or blank.
        """

        registered_subject = kwargs.get("registered_subject")        

        # category of the membership form. Can be any value as long as 
        # it helps link membership forms in some way. For example, 
        # to distinguish 'maternal' from 'infant' forms. Specified at the form level
        membership_form_category = kwargs.get("membership_form_category")        

        if membership_form_category:
            #  membership form 'category' should be a valid subject type found in registered_subject ... and definitely not blank.
            if super(ScheduleGroupManager, self).all():
                if not super(ScheduleGroupManager, self).filter(membership_form__category__icontains = membership_form_category):
                    raise ValueError('The given membership_form_category is not valid for attribute \'category\' in model membership form. Got \'%s\'.' % membership_form_category)            

        # a list of "keys" that link like membership forms together. If they share this 
        # key it means that only one form should be KEYED per subject. 
        # If form is KEYED for subject, there is no need to list the others as UNKEYED        
        # Specified at the scheduledgroup level
        grouping_keys = []

        # a list of KEYED forms
        keyed_membership_forms = {}
        
        #get KEYED schedule group membership forms
        for schedule_group in super(ScheduleGroupManager, self).all():
            membership_form_model = schedule_group.membership_form.content_type_map.model_class()
            if 'registered_subject' in [f.name for f in membership_form_model._meta.fields]:
                if membership_form_model.objects.filter(registered_subject = registered_subject):
                    # append grouping key for schedule groups 
                    # where the membership_form is KEYED and the schedule group 
                    # has more than one membership_form
                    if schedule_group.grouping_key:
                        grouping_keys.append(schedule_group.grouping_key)
                    # add KEYED model 
                    keyed_membership_forms[schedule_group.membership_form.content_type_map.name] = membership_form_model.objects.get(registered_subject = registered_subject) 
            else:
                # raise error is attribute is missing
                raise AttributeError('Membership forms require attribute \'registered_subject\'. Model \'%s\' does not have this attribute but is listed as a membership form.' % schedule_group.membership_form.content_type_map.name)        
        
        #get UNKEYED schedule group membership forms            
        # ...use the grouping key to eliminate membership forms related to a KEYED membership form from above
        qset = (
            Q(membership_form__category__icontains = membership_form_category) |
            Q(membership_form__category__isnull = True) |
            Q(membership_form__category__exact = '')
            )
        schedule_groups = super(ScheduleGroupManager, self).filter(qset)
        unkeyed_membership_forms = [schedule_group.membership_form.content_type_map 
                                    for schedule_group in schedule_groups 
                                        if schedule_group.grouping_key not in grouping_keys and schedule_group.membership_form.content_type_map.name not in keyed_membership_forms]
        return {'keyed': keyed_membership_forms, 'unkeyed':unkeyed_membership_forms}
            
