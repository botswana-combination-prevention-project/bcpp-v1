import logging
import re
from django.utils.encoding import force_unicode
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponseRedirect
from bhp_entry_rules.classes import rule_groups
from bhp_supplemental_fields.models import Excluded
from bhp_data_manager.models import ModelHelpText
from bhp_entry.classes import ScheduledEntry
from bhp_base_admin.exceptions import NextUrlError

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseModelAdmin (admin.ModelAdmin):

    instructions = ['Please complete the questions below.']
    required_instructions = ('Required questions are in bold. '
                             'When all required data has been entered click SAVE to return to the dashboard '
                             'or SAVE NEXT to go to the next form (if available). Additional questions may be required or may need to be corrected when you attempt to save.')

    def __init__(self, *args):
        self._excluded_supplemental_fields = None
        if not isinstance(self.instructions, list):
            raise ImproperlyConfigured('ModelAdmin {0} attribute \'instructions\' must be a list.'.format(self.__class__))
        if not isinstance(self.required_instructions, basestring):
            raise ImproperlyConfigured('ModelAdmin {0} attribute \'required_instructions\' must be a list.'.format(self.__class__))
        super(BaseModelAdmin, self).__init__(*args)

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
        if self.get_excluded_supplemental_fields(obj):
            if self.form._meta.exclude:
                # record which instances were selected for excluded fields, (see also the post_delete signal).
                if Excluded.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk):
                    excluded = Excluded.objects.get(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk)
                    excluded.excluded = self.get_excluded_supplemental_fields(obj)
                    excluded.save()
                else:
                    Excluded.objects.create(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk, excluded=self.get_excluded_supplemental_fields(obj))
            self.form._meta.exclude = None
            self._excluded_supplemental_fields = None

    def add_view(self, request, form_url='', extra_context=None):
        META = 0
        DCT = 1
        extra_context = extra_context or {}
        self._excluded_supplemental_fields = None
        if self.get_excluded_supplemental_fields():
            extra_context['has_excluded_supplemental_fields'] = True
        extra_context['instructions'] = self.instructions
        extra_context['required_instructions'] = self.required_instructions
        extra_context['form_language_code'] = request.GET.get('form_language_code', '')
        if request.GET.get('group_title'):
            extra_context['title'] = ('{group_title}: Add {title}').format(group_title=request.GET.get('group_title'), title=force_unicode(self.model._meta.verbose_name))
        extra_context.update(self.get_dashboard_context(request))
        model_help_text = self.get_model_help_text(self.model._meta.app_label, self.model._meta.object_name)
        extra_context.update(model_help_text_meta=model_help_text[META], model_help_text=model_help_text[DCT])
        return super(BaseModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if self.has_excluded_supplemental_fields(object_id):
            extra_context['has_excluded_supplemental_fields'] = True
        extra_context['instructions'] = self.instructions
        extra_context['required_instructions'] = self.required_instructions
        extra_context['form_language_code'] = request.GET.get('form_language_code', '')
        if request.GET.get('group_title'):
            extra_context['title'] = ('{group_title}: Add {title}').format(group_title=request.GET.get('group_title'), title=force_unicode(self.model._meta.verbose_name))
        extra_context.update(self.get_dashboard_context(request))
        result = super(BaseModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)
        # Look at the referer for a query string '^.*\?.*$'
        ref = request.META.get('HTTP_REFERER', '')
        if ref.find('?') != -1:
            # We've got a query string, set the session value
            request.session['filtered'] = ref
        return result

    def response_add(self, request, obj, post_url_continue=None):
        """Redirects as default unless keyword 'next' is in the GET and is a valid url_name (e.g. can be reversed using other GET values)."""
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        custom_http_response_redirect = None
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            if request.GET.get('next'):
                custom_http_response_redirect = self.response_add_redirect_on_next_url(
                    request.GET.get('next'),
                    request,
                    obj,
                    post_url_continue,
                    post_save=request.POST.get('_save'),
                    post_save_next=request.POST.get('_savenext'),
                    post_cancel=request.POST.get('_cancel'))
        return custom_http_response_redirect or http_response_redirect

    def response_change(self, request, obj, post_url_continue=None):
        """Redirects as default unless keyword 'next' is in the GET and is a valid url_name (e.g. can be reversed using other GET values)."""
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        custom_http_response_redirect = None
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            # look for session variable "filtered" set in change_view
            if request.session.get('filtered', None):
                if 'next=' not in request.session.get('filtered'):
                    # return to the changelist using the same changelist filter, e.g. ?q=Erik
                    custom_http_response_redirect = HttpResponseRedirect(request.session['filtered'])
                    request.session['filtered'] = None
            if request.GET.get('next'):
                # go back to the dashboard or something custom
                custom_http_response_redirect = self.reponse_change_redirect_on_next_url(
                    request.GET.get('next'),
                    request,
                    obj,
                    post_url_continue,
                    post_save=request.POST.get('_save'),
                    post_save_next=request.POST.get('_savenext'),
                    post_cancel=request.POST.get('_cancel'))
        return custom_http_response_redirect or http_response_redirect

    def response_add_redirect_on_next_url(self, next_url_name, request, obj, post_url_continue, post_save=None, post_save_next=None, post_cancel=None):
        """Returns a http_response_redirect when called using the next_url_name.

        Users may override to to add special handling for a named url next_url_name."""
        custom_http_response_redirect = None
        if not next_url_name:
            raise NextUrlError('Attribute \'next_url_name\' may not be none. Check the GET parameter \'next\' in your url.')
        else:
            url = None
            if next_url_name in ['changelist', 'add']:
                # reverse to a default admin url
                # next_url_name is "mode" and is being used to get to the default admin add or changelist
                mode = next_url_name
                app_label = request.GET.get('app_label')
                module_name = request.GET.get('module_name')
                if module_name:
                    module_name = module_name.lower()
                if not app_label or not module_name:
                    raise NextUrlError('next_url_name shortcut \'{0}\' (next={0}) requires GET attributes \'app_label\' and \'module_name\'. Got app_label={1}, module_name={2}.'.format(next_url_name, app_label, module_name))
                url = reverse('admin:{app_label}_{module_name}_{mode}'.format(app_label=app_label, module_name=module_name, mode=mode))
            else:
                try:
                    # try to reverse using the next_url_name and the all values in the GET string
                    # less ['next', 'dashboard_id', 'dashboard_model', 'dashboard_type', 'show'].
                    # dashbord_xx values are excluded because we do not want to intercept a dashboard url here
                    kwargs = {}
                    [kwargs.update({key: value}) for key, value in request.GET.iteritems() if key not in ['next', 'dashboard_id', 'dashboard_model', 'dashboard_type', 'show']]
                    if kwargs:
                        url = reverse(next_url_name, kwargs=kwargs)
                except:
                    # ok, failed to reverse with exactly what was given
                    dashboard_id = request.GET.get('dashboard_id')
                    dashboard_model = request.GET.get('dashboard_model')
                    dashboard_type = request.GET.get('dashboard_type')
                    entry_order = request.GET.get('entry_order')
                    visit_attr = request.GET.get('visit_attr')
                    help_link = request.GET.get('help_link')  # help link added to custom change form
                    show = request.GET.get('show', 'any')

            # at this point we may have a url
            #   1. an admin url (default)
            #   2. a reversed url using next= and all other non-dashboard GET values
            # if we do not have a url, then we have set the dashboard values
            # and will treat the next url as a dashboard url

            if not url:
                if post_save:
                    # will default to a url that takes us back to the subject dashoard below
                    pass
                elif post_save_next:
                    # post_save_next is only available to subject forms
                    # try to reverse using method next_url_in_scheduled_entry_bucket()
                    # which jumps to the next form on the subject dashboard instead of going
                    # back to the subject dashboard
                    try:
                        next_url, visit_model_instance, entry_order = self.next_url_in_scheduled_entry_bucket(obj, visit_attr, entry_order)
                        if next_url:
                            url = ('{next_url}?next={next}&dashboard_type={dashboard_type}&dashboard_id={dashboard_id}'
                                   '&dashboard_model={dashboard_model}&show={show}{visit_attr}{visit_model_instance}{entry_order}{help_link}'
                                   ).format(next_url=next_url,
                                            next=next_url_name,
                                            dashboard_type=dashboard_type,
                                            dashboard_id=dashboard_id,
                                            dashboard_model=dashboard_model,
                                            show=show,
                                            visit_attr='&visit_attr={0}'.format(visit_attr),
                                            visit_model_instance='&{0}={1}'.format(visit_attr, visit_model_instance.pk),
                                            entry_order='&entry_order={0}'.format(entry_order),
                                            help_link='&help_link={0}'.format(help_link))
                    except NoReverseMatch:
                        pass
                elif post_cancel:
                    # cancel goes back to the dashboard
                    # FIXME: i think the URL for the cancel button/link is calculated for by the dashboard
                    #        for the template or reversed on the template, so this might
                    #        be code that cannot be reached
                    url = reverse(
                        'subject_dashboard_url', kwargs={  # TODO: this defaults to the value subject_dashboard_url, not the variable!!!
                        'dashboard_type': dashboard_type,
                        'dashboard_id': dashboard_id,
                        'dashboard_model': dashboard_model,
                        'show': show})
                else:
                    pass
            if not url:
                # default back to the dashboard
                url = self.reverse_next_to_dashboard(next_url_name, request, obj)
            custom_http_response_redirect = HttpResponseRedirect(url)
        return custom_http_response_redirect

    def reponse_change_redirect_on_next_url(self, next_url_name, request, obj, post_url_continue, post_save, post_save_next, post_cancel):
        """Returns an http_response_redirect if next_url_name can be reversed otherwise None.

        Users may override to to add special handling for a named url next_url_name.

        .. note:: currently this assumes the next_url_name is reversible using dashboard criteria or returns nothing."""
        custom_http_response_redirect = None
        if 'dashboard' in next_url_name:   # FIXME: find a better way to intercept dashboard urls and ignore others
            url = self.reverse_next_to_dashboard(next_url_name, request, obj)
            custom_http_response_redirect = HttpResponseRedirect(url)
            request.session['filtered'] = None
        else:
            kwargs = {}
            [kwargs.update({key: value}) for key, value in request.GET.iteritems() if key != 'next']
            url = reverse(next_url_name, kwargs=kwargs)
            custom_http_response_redirect = HttpResponseRedirect(url)
            request.session['filtered'] = None
        return custom_http_response_redirect

    def set_excluded_supplemental_fields(self, obj):
        self._excluded_supplemental_fields = None
        if 'supplemental_fields' in dir(self):
            # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
            if 'exclude' in dir(self.form.Meta):
                raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
            # always set to None first
            self.form._meta.exclude = None
            self.fields, self._excluded_supplemental_fields = self.supplemental_fields.choose_fields(self.fields, self.form._meta.model, obj)

    def get_excluded_supplemental_fields(self, obj=None):
        if not self._excluded_supplemental_fields:
            self.set_excluded_supplemental_fields(obj)
        return self._excluded_supplemental_fields

    def has_excluded_supplemental_fields(self, object_id):
        return Excluded.objects.filter(model_pk=object_id).exists()

    def get_form(self, request, obj=None, **kwargs):
        """Overrides to check if conditional and supplemental fields have been defined in the admin class.

            * get_form is called once to render and again to save, e.g. on GET and then on POST.
            * Need to be sure that the same conditional and/or supplemental choice is given on GET and POST for both
              add and change.
        """
#         exclude_conditional_fields = None
        #exclude_supplemental_fields = None
        if not request.method == 'POST':
            #exclude_conditional_fields = None
            #exclude_supplemental_fields = None
#             if 'conditional_fields' in dir(self):
#                 # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
#                 if 'exclude' in dir(self.form.Meta):
#                     raise AttributeError('The form.Meta attribute exclude cannot be used with \'conditional_fields\'. See {0}.'.format(self.form))
#                 # always set to None first
#                 self.form._meta.exclude = None
#                 self.fields, exclude_conditional_fields = self.conditional_fields.choose_fields(self.fields, self.form._meta.model, obj)
            #self.get_excluded_supplemental_fields(obj)
#             if exclude_conditional_fields:
#                 # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
#                 self.form._meta.exclude = exclude_conditional_fields
            if self.get_excluded_supplemental_fields(obj):
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                if self.form._meta.exclude:
                    self.form._meta.exclude = tuple(set(list(self.form._meta.exclude) + list(self.get_excluded_supplemental_fields(obj))))
                else:
                    self.form._meta.exclude = self.get_excluded_supplemental_fields(obj)
        form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
        form = self.auto_number(form)
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

    def reverse_next_to_dashboard(self, next_url_name, request, obj, **kwargs):
        url = ''
        if next_url_name and request.GET.get('dashboard_id') and request.GET.get('dashboard_model') and request.GET.get('dashboard_type'):
            kwargs = {'dashboard_id': request.GET.get('dashboard_id'),
                      'dashboard_model': request.GET.get('dashboard_model'),
                      'dashboard_type': request.GET.get('dashboard_type')}
            # a subject dashboard url will also have "show"
            if request.GET.get('show'):  # this may fail if a subject template does not set show
                kwargs.update({'show': request.GET.get('show', 'any')})
            url = reverse(next_url_name, kwargs=kwargs)
        elif next_url_name in ['changelist', 'add']:
            app_label = request.GET.get('app_label')
            module_name = request.GET.get('module_name').lower()
            mode = next_url_name
            url = reverse('admin:{app_label}_{module_name}_{mode}'.format(app_label=app_label, module_name=module_name, mode=mode))
        else:
            # normally you should not be here.
            try:
                kwargs = self.convert_get_to_kwargs(request, obj)
                url = reverse(next_url_name, kwargs=kwargs)
            except NoReverseMatch:
                raise NoReverseMatch('response_add failed to reverse url \'{0}\' with kwargs {1}. Is this a dashboard url?'.format(next_url_name, kwargs))
                #logger.warning('Warning: response_add failed to reverse \'{0}\' with kwargs {1}'.format(next_url_name, kwargs))
                #pass
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

    def get_model_help_text(self, app_label=None, module_name=None):
        mht = {}
        for model_help_text in ModelHelpText.objects.filter(app_label=app_label, module_name=module_name.lower()):
            mht.update({model_help_text.field_name: model_help_text})
        return (ModelHelpText._meta, mht)

    def next_url_in_scheduled_entry_bucket(self, obj, visit_attr, entry_order):
        """Returns a tuple with the reverse of the admin url for the next model listed in scheduled_entry_bucket.

        If there is not a "next" model, returns an empty tuple (None, None, None).

        Called from response_add and response_change."""
        retval = (None, None, None)
        if not visit_attr or not entry_order:
            return retval
        visit_model_inst = getattr(obj, visit_attr)
        self.run_rule_groups(visit_model_inst)
        scheduled_entry_bucket = ScheduledEntry().get_next_entry_for(entry_order, visit_model_inst.get_appointment(), visit_model_inst.appointment.get_registered_subject())
        if scheduled_entry_bucket:
            url = reverse('admin:{0}_{1}_add'.format(scheduled_entry_bucket.entry.content_type_map.app_label, scheduled_entry_bucket.entry.content_type_map.module_name))
            retval = (url, visit_model_inst, scheduled_entry_bucket.entry.entry_order)
        return retval

    def run_rule_groups(self, visit_model_instance):
        """ Runs rules in any rule groups for a given visit model instance."""
        if visit_model_instance:
            rule_groups.update_all(visit_model_instance)
