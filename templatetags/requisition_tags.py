from datetime import *
from dateutil.relativedelta import *
from django import template
from django.core.urlresolvers import reverse
from django.db.models import get_model, ForeignKey
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.base import ModelBase

register = template.Library()


class RequisitionModeAdminUrl(template.Node):

    """return a reverse url to requisition in admin + '?dashboard-specific querystring' for 'change' or 'add' for a given panele"""

    def __init__(self, requisition_model, panel, registered_subject, appointment, visit_model, dashboard_type):
        self.unresolved_requisition_model = template.Variable(requisition_model)
        self.unresolved_panel = template.Variable(panel)        
        self.unresolved_registered_subject = template.Variable(registered_subject)
        self.unresolved_appointment = template.Variable(appointment)                
        self.unresolved_visit_model = template.Variable(visit_model)        
        self.unresolved_dashboard_type = template.Variable(dashboard_type)

    def render(self, context):
        self.requisition_model = self.unresolved_requisition_model.resolve(context)
        self.panel = self.unresolved_panel.resolve(context)        
        self.registered_subject = self.unresolved_registered_subject.resolve(context)       
        self.appointment = self.unresolved_appointment.resolve(context)                
        self.visit_model = self.unresolved_visit_model.resolve(context)        
        self.dashboard_type = self.unresolved_dashboard_type.resolve(context)
        
        self.requisition_model = self.requisition_model.__class__
        
        if self.visit_model.__class__.objects.filter(appointment = self.appointment):
            self.visit_model_instance = self.visit_model.__class__.objects.get(appointment = self.appointment)

        this_model_fk = [fk for fk in [f for f in self.requisition_model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if this_model_fk:
            # get the name of the field, e.g. visit or maternal_visit ...
            fk_fieldname_to_visit_model = '%s_id' % this_model_fk[0].name
        else:
            raise AttributeError, 'Cannot determine pk with this templatetag, Model %s must have a foreignkey to the visit model \'%s\'.'
        
        if self.requisition_model.objects.extra(where=[fk_fieldname_to_visit_model+'=%s','panel_id=%s'], params=[self.visit_model_instance.pk, self.panel.pk]):        
            #the link is for a change
            # these next two lines would change if for another dashboard and another visit model 
            next = 'dashboard_visit_url'
            this_model_instance = self.requisition_model.objects.extra(where=[fk_fieldname_to_visit_model+'=%s','panel_id=%s'], params=[self.visit_model_instance.pk, self.panel.pk])
            # do reverse url
            view = 'admin:%s_%s_change' % (self.requisition_model._meta.app_label, self.requisition_model._meta.module_name)
            view = str(view)
            rev_url = reverse(view, args=(this_model_instance[0].pk,))
            # add GET string to rev_url so that you will return to the dashboard ...whence you came... assuming you catch "next" in change_view
            rev_url = '%s?next=%s&dashboard_type=%s&subject_identifier=%s&visit_code=%s&visit_instance=%s&panel=%s' % (
                                                                       rev_url, next, self.dashboard_type, 
                                                                       self.visit_model_instance.appointment.registered_subject.subject_identifier, 
                                                                       self.visit_model_instance.appointment.visit_definition.code, 
                                                                       self.visit_model_instance.appointment.visit_instance,
                                                                       self.panel.pk )            
        else:

            # find the attribute that in this model that is the foreignkey to the visit_model

            # the link is for an add
            next = 'dashboard_visit_add_url'
            #visit_model = get_model(self.app_label, 'Visit').objects.get(pk = self.visit_pk)
            
            view = 'admin:%s_%s_add' % (self.requisition_model._meta.app_label, self.requisition_model._meta.module_name)
            view = str(view)
            rev_url = reverse(view)
            rev_url = '%s?%s=%s&next=%s&dashboard_type=%s&subject_identifier=%s&visit_code=%s&visit_instance=%s&panel=%s' % (
                                                                        rev_url, this_model_fk[0].name,
                                                                        self.visit_model_instance.pk, next, self.dashboard_type, 
                                                                        self.visit_model_instance.appointment.registered_subject.subject_identifier, 
                                                                        self.visit_model_instance.appointment.visit_definition.code, 
                                                                        self.visit_model_instance.appointment.visit_instance,
                                                                        self.panel.pk)            
            #except:
            #    raise TypeError('NoReverseMatch while rendering reverse for %s_%s in RequisitionModeAdminUrl. Is model registered in admin?' % (self.requisition_model._meta.app_label, self.requisition_model._meta.module_name))    
        return rev_url

@register.tag(name='requisition_model_admin_url')
def requisition_model_admin_url(parser, token):

    """Compilation function for renderer RequisitionModeAdminUrl """ 

    try:
        tag_name, requisition_model, panel, registered_subject, appointment, visit_model, dashboard_type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 6 arguments" % token.contents.split()[0])
    return RequisitionModeAdminUrl(requisition_model, panel, registered_subject, appointment, visit_model, dashboard_type)


class GetRequisitionValue(template.Node):

    """return a requisition identifier"""

    def __init__(self, field_name,requisition_model, panel, registered_subject, appointment, visit_model):
        self.unresolved_field_name = template.Variable(field_name)
        self.unresolved_requisition_model = template.Variable(requisition_model)
        self.unresolved_panel = template.Variable(panel)        
        self.unresolved_registered_subject = template.Variable(registered_subject)
        self.unresolved_appointment = template.Variable(appointment)                
        self.unresolved_visit_model = template.Variable(visit_model)        

    def render(self, context):
        self.field_name = self.unresolved_field_name.resolve(context)
        self.requisition_model = self.unresolved_requisition_model.resolve(context)
        self.panel = self.unresolved_panel.resolve(context)        
        self.registered_subject = self.unresolved_registered_subject.resolve(context)       
        self.appointment = self.unresolved_appointment.resolve(context)                
        self.visit_model = self.unresolved_visit_model.resolve(context)        
        
        self.requisition_model = self.requisition_model.__class__
        
        if self.visit_model.__class__.objects.filter(appointment = self.appointment):
            self.visit_model_instance = self.visit_model.__class__.objects.get(appointment = self.appointment)

        this_model_fk = [fk for fk in [f for f in self.requisition_model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if this_model_fk:
            # get the name of the field, e.g. visit or maternal_visit ...
            fk_fieldname_to_visit_model = '%s_id' % this_model_fk[0].name
        else:
            raise AttributeError, 'Cannot determine pk with this templatetag, Model %s must have a foreignkey to the visit model \'%s\'.'
        
        req = self.requisition_model.objects.extra(where=[fk_fieldname_to_visit_model+'=%s','panel_id=%s'], params=[self.visit_model_instance.pk, self.panel.pk])
        if req:        
            return getattr(req[0], self.field_name)
        else:
            return 'not drawn'

@register.tag(name='get_requisition_value')
def get_requisition_value(parser, token):

    """Compilation function for renderer GetRequisitionIdentifier """ 

    try:
        tag_name, field_name, requisition_model, panel, registered_subject, appointment, visit_model = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 6 arguments" % token.contents.split()[0])
    return GetRequisitionValue(field_name, requisition_model, panel, registered_subject, appointment, visit_model)

