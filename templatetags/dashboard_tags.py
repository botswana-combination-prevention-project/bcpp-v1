from datetime import *
from dateutil.relativedelta import *
from django import template
from django.core.urlresolvers import reverse
from django.db.models import get_model 

register = template.Library()


class ModelAdminUrl(template.Node):

    """return a reverse url to admin + '?dashboard-specific querystring' for 'change' or 'add' for a given contenttype model name"""

    def __init__(self, contenttype, visit_pk, dashboard, app_label):
        self.unresolved_contenttype = template.Variable(contenttype)
        self.unresolved_visit_pk = template.Variable(visit_pk)
        self.unresolved_dashboard = template.Variable(dashboard)
        self.unresolved_app_label = template.Variable(app_label)
    def render(self, context):
        self.contenttype = self.unresolved_contenttype.resolve(context)
        self.visit_pk = self.unresolved_visit_pk.resolve(context)
        self.dashboard = self.unresolved_dashboard.resolve(context)
        self.app_label = self.unresolved_app_label.resolve(context)
        if self.contenttype.model_class().objects.filter(visit = self.visit_pk):
            #the link is for a change
            # these next two lines would change if for another dashboard and another visit model 
            next = 'dashboard_visit_url'
            model = self.contenttype.model_class().objects.get(visit = self.visit_pk)
            visit_model = model.visit        
            # do reverse url
            view = 'admin:%s_%s_change' % (self.contenttype.app_label, self.contenttype.model)
            view = str(view)
            rev_url = reverse(view, args=(model.pk,))
            # add GET string to rev_url so that you will return to the dashboard ...whence you came... assuming you catch "next" in change_view
            rev_url = '%s?next=%s&dashboard=%s&subject_identifier=%s&visit_code=%s&visit_instance=%s' % (rev_url, next, self.dashboard, visit_model.appointment.registered_subject.subject_identifier, visit_model.appointment.visit_definition.code, visit_model.appointment.visit_instance )            
        else:
            # the link is for an add
            next = 'dashboard_visit_add_url'
            visit_model = get_model(self.app_label, 'Visit').objects.get(pk = self.visit_pk)
            view = 'admin:%s_%s_add' % (self.contenttype.app_label, self.contenttype.model)
            view = str(view)
            try:
                rev_url = reverse(view)
                rev_url = '%s?visit=%s&next=%s&dashboard=%s&subject_identifier=%s&visit_code=%s&visit_instance=%s' % (rev_url, self.visit_pk, next, self.dashboard, visit_model.appointment.registered_subject.subject_identifier, visit_model.appointment.visit_definition.code, visit_model.appointment.visit_instance)            
            except:
                raise TypeError('NoReverseMatch while rendering reverse for %s_%s in admin_url_from_contenttype. Is model registered in admin?' % (self.contenttype.app_label, self.contenttype.model))    
        return rev_url

@register.tag(name='model_admin_url')
def model_admin_url(parser, token):

    """Compilation function for renderer ModelAdminUrl""" 

    try:
        tag_name, contenttype, visit_pk, dashboard, app_label = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 4 arguments" % token.contents.split()[0])
    return ModelAdminUrl(contenttype, visit_pk, dashboard, app_label)



def appointment_row(context,appointment):

    """Given an apointment instance, render to template an appointment/visit report row for the clinic dashboard."""

    my_context = {}
    my_context['appointment'] = appointment        
    my_context['visit_model_instance'] = None   
    my_context['appointment_visit_report'] = False
    my_context['dashboard'] = context['dashboard']
    my_context['subject_identifier'] = context['subject_identifier']
    my_context['registered_subject'] = context['registered_subject']
    my_context['app_label'] = context['app_label']    
    
    visit_model = get_model(context['app_label'], context['visit_model_name'])
    
    if visit_model.objects.filter(appointment = appointment):
    
        my_context['visit_model_instance'] = visit_model.objects.get(appointment = appointment)
        my_context['appointment_visit_report'] = True

    return my_context        
register.inclusion_tag('appointment_row.html', takes_context=True)(appointment_row)        

