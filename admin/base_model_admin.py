import logging
import re
from django.contrib import admin
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponseRedirect
from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
from bhp_supplemental_fields.models import Excluded

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseModelAdmin (admin.ModelAdmin):

    instructions = 'Please complete the questions below.'
    required_instructions = 'Required questions are in bold. Additional questions may be required based on submitted data.'

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
        if 'supplemental_fields' in dir(self) or 'conditional_fields' in dir(self):
            if self.form._meta.exclude:
                # record which instances were selected for excluded fields, (see also the post_delete signal).
                Excluded.objects.get_or_create(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk, excluded=self.form._meta.exclude)
            self.form._meta.exclude = None

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['instructions'] = self.instructions
        extra_context['required_instructions'] = self.required_instructions
        extra_context.update(self.get_dashboard_context(request))
        return super(BaseModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['instructions'] = self.instructions
        extra_context['required_instructions'] = self.required_instructions
        extra_context.update(self.get_dashboard_context(request))
        result = super(BaseModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)
        # Look at the referer for a query string '^.*\?.*$'
        ref = request.META.get('HTTP_REFERER', '')
        if ref.find('?') != -1:
            # We've got a query string, set the session value
            request.session['filtered'] = ref
        return result

    def response_add(self, request, obj, post_url_continue=None):
        """Redirects if keyword 'next' is a url name that can be reversed.

        Important:
        1. the value of next is NOT a url but a 'url name' where kwargs has
           the keyword/values needed to reverse the 'url name'.
        2. All keyword/values must be used for the reverse (except 'next' and 'csrfmiddlewaretoken').

        Example:
            In your urls.py a named url such as "survey_section_url":

                url(r'^(?P<section_name>household|mobile|statistics|administration)/(?P<survey>mpp\-year\-[0-9]{1}|mobile\-year\-[0-9]{1})/$',
                    'section_index', name="survey_section_url"),

            In your template, refer to this named url and provide the kwargs as hidden input tags.
                <form method="GET" action="/admin/mochudi_household/household/add/">
                    {% csrf_token %}
                    <input type='hidden' name="survey" value="{{selected_survey.survey_slug}}">
                    <input type='hidden' name="next" value="survey_section_url">
                    <input type="hidden" name="section_name" value="{{section_name}}">
                    <input type="submit" value="Create new household" class="default" />
                </form>
        """

        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            if request.GET.get('next'):
                url = None
                dashboard_id = request.GET.get('dashboard_id')
                dashboard_model = request.GET.get('dashboard_model')
                dashboard_type = request.GET.get('dashboard_type')
                entry_order = request.GET.get('entry_order')
                visit_attr = request.GET.get('visit_attr')
                show = request.GET.get('show', 'any')
                if '_savenext' in request.POST:
                    # go to the next form
                    next_url, visit_model_instance, entry_order = RegisteredSubjectDashboard().next_url_in_scheduled_entry_bucket(obj, visit_attr, entry_order, dashboard_type, dashboard_id, dashboard_model)
                    if next_url:
                        url = ('{next_url}?next={next}&dashboard_type={dashboard_type}&dashboard_id={dashboard_id}'
                               '&dashboard_model={dashboard_model}&show=forms{visit_attr}{visit_model_instance}{entry_order}'
                               ).format(next_url=next_url,
                                        next=request.GET.get('next'),
                                        dashboard_type=dashboard_type,
                                        dashboard_id=dashboard_id,
                                        dashboard_model=dashboard_model,
                                        visit_attr='&visit_attr={0}'.format(visit_attr),
                                        visit_model_instance='&{0}={1}'.format(visit_attr, visit_model_instance.pk),
                                        entry_order='&entry_order={0}'.format(entry_order))
                if '_cancel' in request.POST:
                    url = reverse('subect_dashboard_url', kwargs={'dashboard_type': dashboard_type,
                                                                  'dashboard_id': dashboard_id,
                                                                  'dashboard_model': dashboard_model,
                                                                  'show': show})
                if not url:
                    # go back to the dashboard
                    url = self.reverse_next_to_dashboard(request, obj)
                http_response_redirect = HttpResponseRedirect(url)
        return http_response_redirect

    def response_change(self, request, obj, post_url_continue=None):
        """Redirects if keyword 'next' is a url name that can be reversed.

        See comment for response_add() above"""
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            # look for session variable "filtered" set in change_view
            if request.session.get('filtered', None):
                if 'next=' not in request.session.get('filtered'):
                    http_response_redirect = HttpResponseRedirect(request.session['filtered'])
                    request.session['filtered'] = None
            if request.GET.get('next'):
                # go back to the dashboard
                url = self.reverse_next_to_dashboard(request, obj)
                http_response_redirect = HttpResponseRedirect(url)
                request.session['filtered'] = None
        return http_response_redirect

    def get_form(self, request, obj=None, **kwargs):
        """Overrides to check if conditional and supplemental fields have been defined in the admin class.

            * get_form is called once to render and again to save, e.g. on GET and then on POST.
            * Need to be sure that the same conditional and/or supplemental choice is given on GET and POST for both
              add and change.
        """
        exclude_conditional_fields = None
        exclude_supplemental_fields = None
        if not request.method == 'POST':
            exclude_conditional_fields = None
            exclude_supplemental_fields = None
            if 'conditional_fields' in dir(self):
                # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
                if 'exclude' in dir(self.form.Meta):
                    raise AttributeError('The form.Meta attribute exclude cannot be used with \'conditional_fields\'. See {0}.'.format(self.form))
                # always set to None first
                self.form._meta.exclude = None
                self.fields, exclude_conditional_fields = self.conditional_fields.choose_fields(self.fields, self.form._meta.model, obj)
            if 'supplemental_fields' in dir(self):
                # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
                if 'exclude' in dir(self.form.Meta):
                    raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
                # always set to None first
                self.form._meta.exclude = None
                self.fields, exclude_supplemental_fields = self.supplemental_fields.choose_fields(self.fields, self.form._meta.model, obj)
            if exclude_conditional_fields:
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                self.form._meta.exclude = exclude_conditional_fields
            if exclude_supplemental_fields:
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                if self.form._meta.exclude:
                    self.form._meta.exclude = tuple(set(list(self.form._meta.exclude) + list(exclude_supplemental_fields)))
                else:
                    self.form._meta.exclude = exclude_supplemental_fields
        form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
        form = self.auto_number(form)
        #form = self.insert_translation_help_text(form)
        return form

    def update_modified_stamp(self, request, obj, change):
        """Forces username to be saved on add/change and other stuff, called from save_model"""
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()

    def insert_translation_help_text(self, form):
        WIDGET = 1
        for fld in form.base_fields.iteritems():
            fld[WIDGET].translation_help_text = unicode('translation')
        return form

    def auto_number(self, form):
        WIDGET = 1
        auto_number = True
        if 'auto_number' in dir(form._meta):
            auto_number = form._meta.auto_number
        if auto_number:
            for index, fld in enumerate(form.base_fields.iteritems()):
                if not re.match(r'^\d+\.', unicode(fld[WIDGET].label)):
                    fld[WIDGET].label = '{0}. {1}'.format(unicode(index + 1), unicode(fld[WIDGET].label))
        return form

    def get_dashboard_context(self, request):
        return {'subject_dashboard_url': request.GET.get('next', ''),
                      'dashboard_type': request.GET.get('dashboard_type', ''),
                      'dashboard_model': request.GET.get('dashboard_model', ''),
                      'dashboard_id': request.GET.get('dashboard_id', ''),
                      'show': request.GET.get('show', 'any')}

    def reverse_next_to_dashboard(self, request, obj, **kwargs):
        url = ''
        if request.GET.get('next') and request.GET.get('dashboard_id') and request.GET.get('dashboard_model') and request.GET.get('dashboard_type'):
            url = reverse(request.GET.get('next'), kwargs={'dashboard_id': request.GET.get('dashboard_id'),
                                                           'dashboard_model': request.GET.get('dashboard_model'),
                                                           'dashboard_type': request.GET.get('dashboard_type'),
                                                           'show': request.GET.get('show', 'any')})
        else:
            # normally you should not be here.
            try:
                kwargs = self.convert_get_to_kwargs(request, obj)
                url = reverse(request.GET.get('next'), kwargs=kwargs)
            except NoReverseMatch:
                raise NoReverseMatch('response_add failed to reverse \'{0}\' with kwargs {1}'.format(request.GET.get('next'), kwargs))
                logger.warning('Warning: response_add failed to reverse \'{0}\' with kwargs {1}'.format(request.GET.get('next'), kwargs))
                pass
            except:
                raise
        return url

    def convert_get_to_kwargs(self, request, obj):
        kwargs = {}
        for k, v in request.GET.iteritems():
            kwargs[str(k)] = ''.join(unicode(i) for i in request.GET.get(k))
            if not v:
                if k in dir(obj):
                    try:
                        kwargs[str(k)] = getattr(obj, k)
                    except:
                        pass
        if 'next' in kwargs:
            del kwargs['next']
        if 'csrfmiddlewaretoken' in kwargs:
            del kwargs['csrfmiddlewaretoken']
        return kwargs
