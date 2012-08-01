from datetime import *
from dateutil.relativedelta import *
from django import template
from django.core.urlresolvers import reverse
from django.db.models import ForeignKey

register = template.Library()


def appointment_row(context, appointment):

    """Given an apointment instance, render to template an appointment/visit report row for the clinic dashboard."""

    my_context = {}
    my_context['appointment'] = appointment
    my_context['visit_model_instance'] = None
    my_context['visit_code'] = context['visit_code']
    my_context['visit_instance'] = context['visit_instance']
    my_context['appointment_visit_report'] = False
    my_context['dashboard_type'] = context['dashboard_type']
    my_context['subject_identifier'] = context['subject_identifier']
    my_context['registered_subject'] = context['registered_subject']
    my_context['app_label'] = context['app_label']
    my_context['visit_model'] = context['visit_model']
    my_context['visit_model_add_url'] = context['visit_model_add_url']
    my_context['extra_url_context'] = context['extra_url_context']

    visit_model = my_context['visit_model']
    if visit_model.objects.filter(appointment=appointment):
        my_context['visit_model_instance'] = visit_model.objects.get(appointment=appointment)
        my_context['appointment_visit_report'] = True

    return my_context
register.inclusion_tag('appointment_row.html', takes_context=True)(appointment_row)


class ModelPk(template.Node):
    def __init__(self, contenttype, visit_model, appointment, dashboard_type, app_label):
        self.unresolved_contenttype = template.Variable(contenttype)
        self.unresolved_appointment = template.Variable(appointment)
        self.unresolved_visit_model = template.Variable(visit_model)
        self.unresolved_dashboard_type = template.Variable(dashboard_type)
        self.unresolved_app_label = template.Variable(app_label)

    def render(self, context):
        self.contenttype = self.unresolved_contenttype.resolve(context)
        self.appointment = self.unresolved_appointment.resolve(context)
        self.visit_model = self.unresolved_visit_model.resolve(context)
        self.dashboard_type = self.unresolved_dashboard_type.resolve(context)
        self.app_label = self.unresolved_app_label.resolve(context)
        self.visit_model_instance = None
        pk = None
        try:
            appointment_0 = self.appointment.__class__.objects.get(
                registered_subject=self.appointment.registered_subject,
                visit_definition=self.appointment.visit_definition,
                visit_instance=0)
        except:
            raise TypeError('Registered Subject Dashboard Template tag expected appointment, Got None.')
        if self.visit_model.__class__.objects.filter(appointment=self.appointment):
            self.visit_model_instance = self.visit_model.__class__.objects.filter(appointment=appointment_0)[0]
        this_model = self.contenttype.model_class()
        # find the attribute that in this model that is the foreignkey to the visit_model
        this_model_fk = [fk for fk in [f for f in this_model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if this_model_fk:
            # get the name of the field, e.g. visit or maternal_visit ...
            fk_fieldname_to_visit_model = '%s_id' % this_model_fk[0].name
        else:
            raise AttributeError, 'Cannot determine pk with this templatetag, Model %s must have a foreignkey to the visit model \'%s\'.'
        # query this_model for visit=this_visit, or whatever the fk_fieldname is
        # i have to use 'extra' because i can only know the fk field name pointing to the visit model at runtime
        if self.visit_model_instance:
            if this_model.objects.extra(where=[fk_fieldname_to_visit_model + '=%s'], params=[self.visit_model_instance.pk]):
                #the link is for a change
                # these next two lines would change if for another dashboard and another visit model 
                next = 'dashboard_visit_url'
                this_model_instance = this_model.objects.extra(where=[fk_fieldname_to_visit_model + '=%s'], params=[self.visit_model_instance.pk])[0]
                pk = this_model_instance.pk
        return pk


@register.tag(name='model_pk')
def model_pk(parser, token):

    """return pk for model instance"""

    try:
        tag_name, contenttype, visit_model, appointment, dashboard_type, app_label = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 5 arguments" % token.contents.split()[0])
    return ModelPk(contenttype, visit_model, appointment, dashboard_type, app_label)



class ModelAdminUrl(template.Node):

    """return a reverse url to admin + '?dashboard-specific querystring' for 'change' or 'add' for a given contenttype model name"""

    def __init__(self, contenttype, visit_model, appointment, dashboard_type, app_label, extra_url_context):
        self.unresolved_contenttype = template.Variable(contenttype)
        #self.unresolved_visit_pk = template.Variable(visit_pk)
        self.unresolved_appointment = template.Variable(appointment)
        self.unresolved_visit_model = template.Variable(visit_model)
        self.unresolved_dashboard_type = template.Variable(dashboard_type)
        self.unresolved_app_label = template.Variable(app_label)
        self.unresolved_extra_url_context = template.Variable(extra_url_context)
    def render(self, context):
        self.contenttype = self.unresolved_contenttype.resolve(context)
        #self.visit_pk = self.unresolved_visit_pk.resolve(context)
        self.appointment = self.unresolved_appointment.resolve(context)
        self.visit_model = self.unresolved_visit_model.resolve(context)
        self.dashboard_type = self.unresolved_dashboard_type.resolve(context)
        self.app_label = self.unresolved_app_label.resolve(context)
        self.extra_url_context = self.unresolved_extra_url_context.resolve(context)
        self.visit_model_instance = None

        if not self.extra_url_context:
            self.extra_url_context = ''

        #raise TypeError(self.visit_model)
        # wait ??  what type of obejct is visit_model??

        if self.visit_model.__class__.objects.filter(appointment=self.appointment):
            self.visit_model_instance = self.visit_model.__class__.objects.get(appointment=self.appointment)

        this_model = self.contenttype.model_class()

        # find the attribute that in this model that is the foreignkey to the visit_model
        this_model_fk = [fk for fk in [f for f in this_model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]

        if this_model_fk:
            # get the name of the field, e.g. visit or maternal_visit ...
            fk_fieldname_to_visit_model = '%s_id' % this_model_fk[0].name
        else:
            raise AttributeError, 'Cannot reverse for model, Model %s must have a foreignkey to the visit model \'%s\'. Check the model for the foreignkey and check the ModelAdmin class for line (visit_model=%s). Also check if this model is incorrectly referenced in bhp_visit.Entry.' % (this_model._meta.object_name, self.visit_model._meta.object_name, self.visit_model._meta.object_name)

        # query this_model for visit=this_visit, or whatever the fk_fieldname is
        # i have to use 'extra' because i can only know the fk field name pointing to the visit model at runtime
        if this_model.objects.extra(where=[fk_fieldname_to_visit_model + '=%s'], params=[self.visit_model_instance.pk]):
            #the link is for a change
            # these next two lines would change if for another dashboard and another visit model 
            next = 'dashboard_visit_url'
            this_model_instance = this_model.objects.extra(where=[fk_fieldname_to_visit_model + '=%s'], params=[self.visit_model_instance.pk])[0]
            # do reverse url
            view = 'admin:%s_%s_change' % (this_model._meta.app_label, this_model._meta.module_name)
            view = str(view)
            rev_url = reverse(view, args=(this_model_instance.pk,))
            # add GET string to rev_url so that you will return to the dashboard ...whence you came... assuming you catch "next" in change_view
            rev_url = '%s?next=%s&dashboard_type=%s&subject_identifier=%s&visit_code=%s&visit_instance=%s%s' % (
                                                                       rev_url, next, self.dashboard_type,
                                                                       self.visit_model_instance.appointment.registered_subject.subject_identifier,
                                                                       self.visit_model_instance.appointment.visit_definition.code,
                                                                       self.visit_model_instance.appointment.visit_instance,
                                                                       self.extra_url_context,
                                                                       )
        else:
            # the link is for an add
            next = 'dashboard_visit_add_url'
            #visit_model = get_model(self.app_label, 'Visit').objects.get(pk = self.visit_pk)

            view = 'admin:%s_%s_add' % (self.contenttype.app_label, self.contenttype.model)
            view = str(view)
            try:
                rev_url = reverse(view)
                rev_url = '%s?%s=%s&next=%s&dashboard_type=%s&subject_identifier=%s&visit_code=%s&visit_instance=%s%s' % (
                                                                        rev_url, this_model_fk[0].name,
                                                                        self.visit_model_instance.pk, next, self.dashboard_type,
                                                                        self.visit_model_instance.appointment.registered_subject.subject_identifier,
                                                                        self.visit_model_instance.appointment.visit_definition.code,
                                                                        self.visit_model_instance.appointment.visit_instance,
                                                                        self.extra_url_context,
                                                                        )

            except:
                raise TypeError('NoReverseMatch while rendering reverse for %s_%s in admin_url_from_contenttype. Is model registered in admin?' % (self.contenttype.app_label, self.contenttype.model))

        return rev_url

@register.tag(name='model_admin_url')
def model_admin_url(parser, token):

    """Compilation function for renderer ModelAdminUrl"""

    try:
        tag_name, contenttype, visit_model, appointment, dashboard_type, app_label, extra_url_context = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 6 arguments" % token.contents.split()[0])
    return ModelAdminUrl(contenttype, visit_model, appointment, dashboard_type, app_label, extra_url_context)



class ModelAdminUrlFromRegisteredSubject(template.Node):

    """return a reverse url to admin + '?dashboard-specific querystring' for 'change' or 'add' for a given contenttype model name"""

    def __init__(self, contenttype, registered_subject, dashboard_type, app_label):
        self.unresolved_contenttype = template.Variable(contenttype)
        self.unresolved_registered_subject = template.Variable(registered_subject)
        self.unresolved_dashboard_type = template.Variable(dashboard_type)
        self.unresolved_app_label = template.Variable(app_label)
    def render(self, context):
        self.contenttype = self.unresolved_contenttype.resolve(context)
        self.registered_subject = self.unresolved_registered_subject.resolve(context)
        self.dashboard_type = self.unresolved_dashboard_type.resolve(context)
        self.app_label = self.unresolved_app_label.resolve(context)

        this_model = self.contenttype.model_class()

        if this_model.objects.filter(registered_subject=self.registered_subject):
            #the link is for a change
            # these next two lines would change if for another dashboard and another visit model 
            next = 'dashboard_url'
            this_model_instance = this_model.objects.get(registered_subject=self.registered_subject)
            # do reverse url
            view = 'admin:%s_%s_change' % (this_model._meta.app_label, this_model._meta.module_name)
            view = str(view)
            rev_url = reverse(view, args=(this_model_instance.pk,))
            # add GET string to rev_url so that you will return to the dashboard ...whence you came... assuming you catch "next" in change_view
            rev_url = '%s?next=%s&dashboard_type=%s&registered_subject=%s' % (
                                                                       rev_url, next, self.dashboard_type,
                                                                       self.registered_subject.pk,
                                                                       )
        else:
            # the link is for an add
            next = 'dashboard_url'
            view = 'admin:%s_%s_add' % (self.contenttype.app_label, self.contenttype.model)
            view = str(view)
            #try:
            rev_url = reverse(view)
            rev_url = '%s?next=%s&dashboard_type=%s&registered_subject=%s' % (
                                                                    rev_url,
                                                                    next, self.dashboard_type,
                                                                    self.registered_subject.pk,
                                                                    )
            #except:
            #    raise TypeError('NoReverseMatch while rendering reverse for %s_%s in admin_url_from_contenttype. Is model registered in admin?' % (self.contenttype.app_label, self.contenttype.model))    
        return rev_url

@register.tag(name='model_admin_url_from_registered_subject')
def model_admin_url_from_registered_subject(parser, token):

    """Compilation function for renderer ModelAdminUrlFromRegisteredSubject """

    try:
        tag_name, contenttype, registered_subject, dashboard_type, app_label = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 4 arguments" % token.contents.split()[0])
    return ModelAdminUrlFromRegisteredSubject(contenttype, registered_subject, dashboard_type, app_label)

class ModelPkFromRegisteredSubject(template.Node):
    def __init__(self, contenttype, visit_model, appointment, dashboard_type, app_label):
        self.unresolved_contenttype = template.Variable(contenttype)
        self.unresolved_registered_subject = template.Variable(registered_subject)
        self.unresolved_dashboard_type = template.Variable(dashboard_type)
        self.unresolved_app_label = template.Variable(app_label)
    def render(self, context):
        self.contenttype = self.unresolved_contenttype.resolve(context)
        self.registered_subject = self.unresolved_appointment.resolve(context)
        self.dashboard_type = self.unresolved_dashboard_type.resolve(context)
        self.app_label = self.unresolved_app_label.resolve(context)
        self.visit_model_instance = None

        pk = None

class ModelPkFromRegisteredSubject(template.Node):
    def __init__(self, contenttype, registered_subject, dashboard_type, app_label):
        self.unresolved_contenttype = template.Variable(contenttype)
        self.unresolved_registered_subject = template.Variable(registered_subject)
        self.unresolved_dashboard_type = template.Variable(dashboard_type)
        self.unresolved_app_label = template.Variable(app_label)
    def render(self, context):
        self.contenttype = self.unresolved_contenttype.resolve(context)
        self.registered_subject = self.unresolved_registered_subject.resolve(context)
        self.dashboard_type = self.unresolved_dashboard_type.resolve(context)
        self.app_label = self.unresolved_app_label.resolve(context)
        pk = None
        this_model = self.contenttype.model_class()
        if this_model.objects.filter(registered_subject=self.registered_subject):
            this_model_instance = this_model.objects.get(registered_subject=self.registered_subject)
            pk = this_model_instance.pk
        return pk

@register.tag(name='model_pk_from_registered_subject')
def model_pk_from_registered_subject(parser, token):

    """return pk for model instance"""

    try:
        tag_name, contenttype, registered_subject, dashboard_type, app_label = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 4 arguments" % token.contents.split()[0])
    return ModelPkFromRegisteredSubject(contenttype, registered_subject, dashboard_type, app_label)


