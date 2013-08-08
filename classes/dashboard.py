import re
import inspect
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from bhp_context.classes import BaseContext
from bhp_base_model.models import BaseModel
from bhp_registration.models import RegisteredSubject


class Dashboard(object):

    context = BaseContext()
    dashboard_identifier = None

    def __init__(self, **kwargs):

        self.search_name = None
        self._dashboard_type = None
        self._template = None
        self._dashboard_id = None
        self._dashboard_model = None
        self._dashboard_model_key = None
        self._dashboard_model_instance = None
        self._dashboard_model_reference = None

    def create(self, **kwargs):
        self.set_dashboard_type(kwargs.get('dashboard_type'))
        self.set_dashboard_id(kwargs.get('dashboard_id'))
        self.set_dashboard_model_key(kwargs.get('dashboard_model'))
        self.set_dashboard_model()
        self.context.add(
            search_name=self.search_name,
            template=self.get_template(),
            dashboard_type=self.get_dashboard_type(),
            dashboard_id=self.get_dashboard_id(),
            dashboard_model=self.get_dashboard_model_key(),
            )

    def get_context_prep(self, **kwargs):
        pass

    def get_create_prep(self, **kwargs):
        pass

    def get_context(self):
        return self.context.values

    def set_dashboard_type(self, value=None):
        self._dashboard_type = value

    def get_dashboard_type(self):
        if not self._dashboard_type:
            self.set_dashboard_type()
        return self._dashboard_type

    def set_dashboard_model(self):
        """Sets the model class given by the dashboard URL."""
        model_name = self.get_dashboard_model_key()
        if isinstance(self.get_dashboard_model_reference(model_name), tuple):
            app_label, model_name = self.get_dashboard_model_reference(model_name)
            self._dashboard_model = models.get_model(app_label, model_name)
        elif issubclass(self.get_dashboard_model_reference(model_name), BaseModel):
            self._dashboard_model = self.get_dashboard_model_reference(model_name)
        else:
            raise TypeError('Dashboard model reference must return a tuple (app_label, model_name) or a model class. Got neither for {0}'.format(model_name))
        if not self._dashboard_model:
            raise TypeError('Dashboard model may not be None')

    def get_dashboard_model(self):
        if not self._dashboard_model:
            self.set_dashboard_model()
        return self._dashboard_model

    def set_dashboard_model_instance(self):
        """Sets the model instance using the model class and pk from the dashboard URL."""
        self._dashboard_model_instance = self.get_dashboard_model().objects.get(pk=self.get_dashboard_id())

    def get_dashboard_model_instance(self):
        if not self._dashboard_model_instance:
            self.set_dashboard_model_instance()
        return self._dashboard_model_instance

    def set_dashboard_id(self, pk):
        """Sets the pk of the dashboard model class given by the dashboard URL."""
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not re_pk.match(pk or ''):
            raise TypeError('Dashboard id must be a uuid (pk)')
        self._dashboard_id = pk

    def get_dashboard_id(self):
        if not self._dashboard_id:
            self.set_dashboard_id()
        return self._dashboard_id

    def add_to_dashboard_model_reference(self, value):
        """Adds additional items to the dictionary.

        This dictionary is used to verify the dashboard_model_key
        coming from the url. We only want ones that we expect."""
        if not isinstance(value, dict):
            raise TypeError('Parameter \'value\' must be a dictionary.')
        for v in value.itervalues():
            if inspect.ismethod(v) and v.__name__ == 'get_visit_model':
                pass
            elif not issubclass(v, BaseModel):
                raise TypeError('Dictionary of {{k, v}} must have value attribute v of base class BaseModel. Got {0} for {1}'.format(type(v), value))
        if not self._dashboard_model_reference:
            self._dashboard_model_reference = {}
        self._dashboard_model_reference.update(value)

    def set_dashboard_model_reference(self):
        """Sets a reference dictionary by updating the user defined dictionary with a default for registered_subject."""
        if not self._dashboard_model_reference:
            self._dashboard_model_reference = {}
        self.add_to_dashboard_model_reference({'registered_subject': RegisteredSubject})

    def get_dashboard_model_reference(self, model_name):
        if not self._dashboard_model_reference:
            self.set_dashboard_model_reference()
        if model_name not in self._dashboard_model_reference:
            raise TypeError(('Dashboard model name {0} is not in the user defined dictionary returned by '
                            'method get_dashboard_model_reference(). Got {1}. Perhaps add this model '
                            'with add_dashboard_model_reference() in your subclass.').format(model_name, self._dashboard_model_reference))
        value = self._dashboard_model_reference.get(model_name)
        if inspect.ismethod(value) and value.__name__ == 'get_visit_model':
            value = value()
        return value

    def set_dashboard_model_key(self, value):
        self._dashboard_model_key = value

    def get_dashboard_model_key(self):
        if not self._dashboard_model_key:
            self.set_dashboard_model_key()
        return self._dashboard_model_key

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

    def get_urlpatterns(self, view, regex, **kwargs):
        """Users must override."""
        raise ImproperlyConfigured('You need to define some dashboard urls.')
