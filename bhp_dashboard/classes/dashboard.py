import copy
import re
import inspect
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import patterns, include, url
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from bhp_common.utils import convert_from_camel
from bhp_section.classes import site_sections
from bhp_context.classes import BaseContext
from bhp_base_model.models import BaseModel
from bhp_registration.models import RegisteredSubject
from bhp_dashboard.exceptions import DashboardModelError


class Dashboard(object):

    context = BaseContext()
    dashboard_name = None  # e.g. 'Dashboard'
    dashboard_url_name = None   # e.g. 'dashboard_url_name'

    def __init__(self, dashboard_type, dashboard_id, dashboard_model, dashboard_type_list=None, dashboard_models=None):

        self.search_name = None  # ??
        self._dashboard_type = None
        self._dashboard_type_list = None
        self._template = None
        self._context_is_set = None  # ??
        self._dashboard_id = None
        self._dashboard_model = None
        self._dashboard_model_name = None
        self._dashboard_model_instance = None
        self._dashboard_models = None
        self._dashboard_name = None
        self._dashboard_url_name = None
        if dashboard_type_list:
            self._set_dashboard_type_list(dashboard_type_list)
        self._section = None
        self._section_name = None
        self._search_type = None
        self._set_dashboard_models(dashboard_models)
        self._set_dashboard_type(dashboard_type)
        self._set_dashboard_model(dashboard_model)
        self._set_dashboard_id(dashboard_id)
        # dashboard model may be the name or the model class
        if isinstance(dashboard_model, basestring):
            self._set_dashboard_model_name(dashboard_model)
        elif issubclass(dashboard_model, BaseModel):
            self._set_dashboard_model(dashboard_model)
        else:
            raise TypeError('Invalid dashboard_model. Expected either a Model class or a name of a model. Got {0}'.format(dashboard_model))

    @classmethod
    def get_urlpatterns(self, pattern_prefix, urlpattern_string_kwargs, view=None, **kwargs):
        """Gets the url_patterns for the dashboard view.

        Called in the urls.py of the local xxxx_dashboard app. For example::

            from django.contrib import admin
            from django.conf.urls.defaults import patterns, url
            from dom_dashboard.classes import InfantDashboard, MaternalDashboard

            urlpattern_string_kwargs = {}
            urlpattern_string_kwargs['dashboard_type'] = 'infant'
            urlpattern_string_kwargs['dashboard_model'] = 'infant_birth'
            urlpatterns = InfantDashboard.get_urlpatterns('dom_dashboard.views', urlpattern_string_kwargs, visit_field_names=['infant_visit', ])

            urlpattern_string_kwargs = {}
            urlpattern_string_kwargs['dashboard_type'] = 'maternal'
            urlpattern_string_kwargs['d-ashboard_model'] = 'maternal_consent'
            urlpatterns += MaternalDashboard.get_urlpatterns('dom_dashboard.views', urlpattern_string_kwargs, visit_field_names=['maternal_visit', ])
        """

        if not self.dashboard_url_name:
            raise ImproperlyConfigured('class attribute \'dashboard_url_name\' may not be None')
        if not pattern_prefix:
            raise ImproperlyConfigured('Parameter \'pattern_prefix\' may not be None. Must be app_label.view_module, (e.g. maikalelo_dashboard.views). See your urls.py.')
        view = view or self.view
        if not view:
            raise ImproperlyConfigured('Parameter \'view\' may not be None. Must be a valid view name, such as \'infant_dashboard\'.')
        if not urlpattern_string_kwargs:
            raise ImproperlyConfigured('Parameter \'urlpattern_string_kwargs\' may not be None.')
        if not isinstance(urlpattern_string_kwargs, dict):
            raise ImproperlyConfigured('Parameter \'urlpattern_string_kwargs\' must be a dictionary. Got {0}'.format(urlpattern_string_kwargs))
        # add default re patterns
        urlpattern_string_kwargs['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'

        # FIXME: need to move to registeredSubjectDashboard as these regexs are
        # specific to it, '|visit|appointment|registered_subject'
        # should use the add_to_urlpattern_string_kwargs()
        # and probably do not need to set these in urls!
        if urlpattern_string_kwargs.get('dashboard_model', None):
            urlpattern_string_kwargs['dashboard_model'] += '|visit|appointment|registered_subject'
        else:
            urlpattern_string_kwargs.update({'dashboard_model': 'visit|appointment|registered_subject'})
        if not urlpattern_string_kwargs.get('dashboard_type', None):
            urlpattern_string_kwargs.update({'dashboard_type': 'subject'})

        # add user patterns
        urlpattern_string_kwargs.update(self.add_to_urlpattern_string_kwargs())
        # add extra key/value to the pattern string, if the user has overriden the method add_to_urlpattern_string
        urlpattern_string = r'^(?P<dashboard_type>{{dashboard_type}})/(?P<dashboard_model>{{dashboard_model}})/(?P<dashboard_id>{{pk}})/{0}$'.format(self.add_to_urlpattern_string())
        urlpatterns = patterns(pattern_prefix,
            url(urlpattern_string.format(**urlpattern_string_kwargs),
                view,
                name=self.dashboard_url_name
                ))
        return urlpatterns

    @classmethod
    def add_to_urlpattern_string(cls):
        """Returns a fragment of a url regular expression to be added to the urlpattern string in :func:`get_urlpatterns`."""
        return ''

    @classmethod
    def add_to_urlpattern_string_kwargs(cls):
        """Returns a dictionary to compliment the url regular expression fragment returned by :func:`add_to_urlpattern_string`."""
        return {}

    def add_to_context(self):
        pass

    def _add_to_context(self):
        self.context.add(template=self.get_template(),
            #section=self.get_section(),
            #section_name=self.get_section_name(),
            #search_type=self.get_search_type(),
            dashboard_type=self.get_dashboard_type(),
            dashboard_id=self.get_dashboard_id(),
            dashboard_model=self.get_dashboard_model_name(),  # yes, we use the name not the model class for the context
            dashboard_model_instance=self.get_dashboard_model_instance(),
            dashboard_name=self.get_dashboard_name(),
            dashboard_url_name=self.get_dashboard_url_name(),
            home_url=self.get_home_url())
        self.add_to_context()

    def get_home_url(self):
        """Returns a home url."""
        return reverse(self.get_dashboard_url_name(), kwargs={'dashboard_type': self.get_dashboard_type(),
                                                              'dashboard_model': self.get_dashboard_model_name(),
                                                              'dashboard_id': self.get_dashboard_id()})

    def _set_dashboard_name(self):
        self._dashboard_name = self.dashboard_name

    def get_dashboard_name(self):
        if not self._dashboard_name:
            self._set_dashboard_name()
        return self._dashboard_name

    def _set_dashboard_url_name(self):
        self._dashboard_url_name = self.dashboard_url_name
        if not self._dashboard_url_name:
            raise ImproperlyConfigured('Class attribute \'dashboard_url_name\' may not be None. Set this on the class declaration for {0}.'.format(self))

    def get_dashboard_url_name(self):
        if not self._dashboard_url_name:
            self._set_dashboard_url_name()
        return self._dashboard_url_name

    def _set_dashboard_type(self, value=None):
        self._dashboard_type = value
        if not isinstance(value, basestring):
            raise TypeError('Expected a string for dashboardtype. Got {0}'.format(value))
        if not self._dashboard_type in self.get_dashboard_type_list():
            raise TypeError('Invalid dashboard type. Expected one of {0}'.format(self.get_dashboard_type_list()))
        if not self._dashboard_type:
            raise TypeError('_dashboard_type may not be None.')

    def get_dashboard_type(self):
        if not self._dashboard_type:
            self._set_dashboard_type()
        return self._dashboard_type

    def set_dashboard_type_list(self):
        pass

    def _set_dashboard_type_list(self, value=None):
        """Users should override to set to a list of valid dashboard types such as [\'maternal\', \'infant\'] or [\'household\']."""
        self._dashboard_type_list = None
        if value:
            self._dashboard_type_list = value
        else:
            self.set_dashboard_type_list()
        if not self._dashboard_type_list:
            raise TypeError('Attribute _dashboard_type_list may not be None. Either override the setter or pass as a list on __init__.')

    def get_dashboard_type_list(self):
        if not self._dashboard_type_list:
            self._set_dashboard_type_list()
        return self._dashboard_type_list

    def _set_dashboard_model(self, value=None):
        """Sets the model class given by the dashboard URL.

        Checks with "func"`get_dashboard_models` if model or model_name is known to the class before using it."""
        self._dashboard_model = None
        if value:
            if isinstance(value, basestring):
                if value in self.get_dashboard_models():
                    self._dashboard_model = self.get_dashboard_models().get(value)
                else:
                    raise DashboardModelError('Unable to determine the dashboard model given model name \'{0}\'. Not listed in {1}.'.format(value, self.get_dashboard_models()))
            elif issubclass(value, BaseModel):
                if convert_from_camel(value._meta.object_name) in self.get_dashboard_models():
                    self._dashboard_model = value
                else:
                    raise DashboardModelError('Model class \'{0}\' is not a valid dashboard model. Not listed in {1}.'.format(value, self.get_dashboard_models()))
            else:
                raise TypeError('Attribute _dashboard_model must be a subclass of BaseModel or a name of a model '
                                'and be a know dashboard model. Got {0}. Expected one of {1}'.format(value, self.get_dashboard_models()))
        if not self._dashboard_model:
            raise DashboardModelError('Dashboard model may not be None')

#         else:
#             model_name = self.get_dashboard_model_name()
#             if isinstance(self.get_dashboard_models(model_name), tuple):
#                 app_label, model_name = self.get_dashboard_models(model_name)
#                 self._dashboard_model = models.get_model(app_label, model_name)
#             if not self._dashboard_model:
#                 if model_name in self.get_dashboard_models():
#                     if issubclass(self.get_dashboard_models(model_name), BaseModel):
#                         self._dashboard_model = self.get_dashboard_models(model_name)

    def get_dashboard_model(self):
        if not self._dashboard_model:
            self._set_dashboard_model()
        return self._dashboard_model

    def _set_dashboard_model_name(self, value=None):
        self._dashboard_model_name = value
        if not value:
            self._dashboard_model_name = convert_from_camel(self.get_dashboard_model()._meta.object_name)
        if not self._dashboard_model_name:
            raise TypeError('_dashboard_model_name may not be None.')

    def get_dashboard_model_name(self):
        if not self._dashboard_model_name:
            self._set_dashboard_model_name()
        return self._dashboard_model_name

    def _set_dashboard_id(self, value=None):
        """Sets the pk of the dashboard model class given by the dashboard URL."""
        if not value:
            TypeError('Parameter \'pk\' may not be None.')
        if not isinstance(value, basestring):
            raise TypeError('Expected a string when setting _dashboard_id. Parameter value must be a valid pk. Got {0}'.format(value))
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not re_pk.match(value or ''):
            raise TypeError('Dashboard id must be a uuid (pk). Got {0}'.format(value))
        self._dashboard_id = value

    def get_dashboard_id(self):
        if not self._dashboard_id:
            self._set_dashboard_id()
        return self._dashboard_id

    def get_context_prep(self, **kwargs):
        pass

    def get_create_prep(self, **kwargs):
        pass

    def set_context(self):
        self._add_to_context()
        self._context_is_set = True

    def get_context(self):
        if not self._context_is_set:
            self.set_context()
        return self.context

    def set_search_type(self):
        self._search_type = self.get_section().get_search_type(self.get_section_name())
        #if not self._search_type:
        #    raise TypeError('Attribute \'self._search_type\' may not be None.')

    def get_search_type(self):
        if not self._search_type:
            self.set_search_type()
        return self._search_type

    def set_section(self, section_name=None):
        """Sets the instance of the section class for the dashboard.

        Call in __init__::

            self.set_section('household')
        """
        if not section_name:
            raise TypeError('Parameter \'section_name\' may not be None. Call set_section in __init__ to set the correct section class for this dashboard.')
        section = site_sections.get(section_name)
        if not section:
            if site_sections.get_section_names() == []:
                raise TypeError('class site_sections is not set up. Call autodoscover first.')
            section = site_sections.get(section_name)
        if not section:
            raise TypeError('Could not find section \'{0}\' in site_sections. You need to define a section class for this name in section.py.'.format(section_name))
        self._section = section()

    def get_section(self):
        if not self._section:
            self.set_section()
        return self._section

    def set_section_name(self):
        self._section_name = self.get_section().get_section_name()

    def get_section_name(self):
        if not self._section_name:
            self.set_section_name()
        return self._section_name

    def set_dashboard_model_instance(self):
        """Sets the model instance using the model class and pk from the dashboard URL."""
        self._dashboard_model_instance = self.get_dashboard_model().objects.get(pk=self.get_dashboard_id())

    def get_dashboard_model_instance(self):
        if not self._dashboard_model_instance:
            self.set_dashboard_model_instance()
        return self._dashboard_model_instance

    def verify_dashboard_model(self, value):
        """Verifies the dashboard model(s) in dictionary \'value\' before adding to the dictionary and throws an exception if unable to verify.

        Users may override to test the model for methods or subclass, etc."""
        pass

    def add_dashboard_model(self, value):
        """Adds additional items to the dashboard models dictionary.

        This dictionary is used to verify the dashboard_model name or class
        coming from the url. We only want ones that we expect."""
        if not value:
            raise TypeError('parameter \'value\' may not be None. Expected a model class or function.')
        if not isinstance(value, dict):
            raise TypeError('Parameter \'value\' must be a dictionary.')
        for name, model_or_func in value.iteritems():
            if (inspect.ismethod(model_or_func) or inspect.isfunction(model_or_func)) and model_or_func.__name__ in ['_get_visit_model', 'get_visit_model']:
                value[name] = value[name]()  # may be a function (that returns a model) TODO: may we allow more than just get_visit_model?
                if not issubclass(value[name], BaseModel):
                    raise TypeError('Expected a subclass of BaseModel from function \'get_visit_model\'. Got {0}.'.format(value))
            elif issubclass(model_or_func, BaseModel):
                pass  # may be a model
            elif isinstance(model_or_func, tuple):
                value[name] = models.get_model(model_or_func[0], model_or_func[1])
            else:
                raise TypeError('Dictionary of {{k, v}} must have value attribute v of base class BaseModel or a method that returns a model class. Got {0} for {1}'.format(type(model_or_func), value))
        self.verify_dashboard_model(value)
        self._dashboard_models.update(value)

    def _set_dashboard_models(self, value=None):
        """Sets a reference dictionary by updating the user defined dictionary with a default for registered_subject.
        """
        if self._dashboard_models == None:
            self._dashboard_models = {}
        self._dashboard_models.update({'registered_subject': RegisteredSubject})
        if value:
            self.add_dashboard_model(value)

    def get_dashboard_models(self, model_name=None):
        if not self._dashboard_models:
            self._set_dashboard_models()
        if model_name:
            if model_name not in self._dashboard_models:
                raise TypeError(('Dashboard model name {0} is not in the user defined dictionary returned by '
                                'method get_dashboard_models(). Got {1}. Perhaps add this model '
                                'with add_dashboard_models() in your subclass.').format(model_name, self._dashboard_models))
            value = self._dashboard_models.get(model_name)
            return value
        return copy.deepcopy(self._dashboard_models)

    def set_template(self, value=None):
        self._template = value
        if not self._template and self.get_dashboard_type():
            self._template = '{0}_dashboard.html'.format(self.get_dashboard_type())
        if not self._template:
            raise TypeError('Attribute _template cannot be None.')

    def get_template(self):
        if not self._template:
            self.set_template()
        return self._template

    def set_extra_url_context(self):
        pass

    def _set_extra_url_context(self):
        """Sets / updates the extra_url_context dictionary."""
        self._extra_url_context = ''
        self.set_extra_url_context()
        # adds the current language
        self._extra_url_context = '{0}&form_language_code={1}'.format(self._extra_url_context, self.get_language())

    def get_extra_url_context(self):
        """Gets the extra_url_context and returns as a GET query string."""
        if not self._extra_url_context:
            self._set_extra_url_context()
        return self._extra_url_context
