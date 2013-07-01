from datetime import datetime, date
#from django.views.base import View  # for 1.5
from django.conf.urls.defaults import patterns as url_patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bhp_appointment.models import Appointment
#from bhp_data_manager.models import ActionItem
from bhp_search.classes import site_search
from bhp_section.exceptions import SectionError


# class Section(View):  # 1.5
class BaseSectionView(object):

    section_name = None
    section_list = None
    section_template = None
    add_model = None

    def __init__(self):
        self._context = {}
        self._template = None
        self._section_name = None
        self._add_model_cls = None
        self._section_list = None
        self.search_label = None
        #self.urlpattern_prepared = False
        self._sections_using_search = []
        self._custom_template = {}
        self._search_type = {}
        self._search_name = {}

    @property
    def context(self):
        return self._context

    def update_context(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._context[k] = v

    def set_section_list(self, value=None):
        if self.section_list:
            # class variable set in urls
            self._section_list = self.section_list
        elif not value:
            raise AttributeError('Attribute \'sections_list\' may not be None. Should be set in urls.py')
        else:
            self._section_list = value

    def get_section_list(self):
        if not self._section_list:
            self.set_section_list()
        return self._section_list

    def set_section_name(self, value=None):
        if self.section_name:
            self._section_name = self.section_name
        else:
            self._section_name = value
        self._set_template()

    def get_section_name(self):
        if not self._section_name:
            self.set_section_name()
        return self._section_name

    def _set_add_model_cls(self, value=None):
        if self.add_model:
            self._add_model_cls = self.add_model
        else:
            self._add_model_cls = value

    def get_add_model_cls(self):
        if not self._add_model_cls:
            self._set_add_model_cls()
        return self._add_model_cls

    def get_add_model_name(self):
        if self.get_add_model_cls():
            return self.get_add_model_cls()._meta.verbose_name
        return None

    def get_add_model_opts(self):
        if self.get_add_model_cls():
            return self.get_add_model_cls()._meta
        return None

    def set_search_type(self, section_name, search_type=None):
        if search_type:
            self._search_type.update({section_name: search_type})

    def get_search_type(self, section_name):
        if not section_name in self._search_type:
            self.set_search_type(section_name)
        if section_name in self._search_type:
            return self._search_type.get(section_name)
        return None

    def set_search_name(self, section_name, search_name=None):
        if search_name:
            self._search_name.update({section_name: search_name})

    def get_search_name(self, section_name):
        if not section_name in self._search_name:
            self.set_search_name(section_name)
        if section_name in self._search_name:
            return self._search_name.get(section_name)
        return None

    def get_sections_using_search(self, section_name=None):
        if section_name:
            if section_name in self._sections_using_search:
                return [section_name]
            else:
                return []
        return self._sections_using_search

    def add_to_sections_using_search(self, section_name):
        if section_name not in self._sections_using_search:
            self._sections_using_search.append(section_name)

    def _set_template(self, template=None):
        if template:
            self._template = template
        elif self.section_template:
            self._template = self.section_template
        else:
            self._template = self._get_default_template()

    def get_template(self):
        if not self._template:
            self._set_template()
        return self._template

    def _get_default_template(self):
        return 'section_{0}.html'.format(self.get_section_name())

    def urlpatterns(self, view=None):
        """ Generates a urlpattern for the view of this subclass."""
        if not site_search.is_autodiscovered:
            raise SectionError('Search register not ready. Call search.autodiscover() first.')
        #self.urlpattern_prepared = True
        if view is None:
            view = self._view
        urlpattern_first = []
        urlpattern_last = []
        #for section_name in section_index_view.get_section_name_list():
        #    # try to match this section to a search class
        section_name = self.get_section_name()
        for search_type, search_cls in site_search.get_registry().iteritems():
            # for each type of search, look for an association with this section_name
            if search_cls().get_section_name() == section_name:
                self.set_search_type(section_name, search_type)
                self.set_search_name(section_name, search_cls().name)
                urlpattern_first += url_patterns(
                    '',
                    url(r'^(?P<section_name>{section_name})/(?P<search_type>{search_type})/$'.format(section_name=section_name, search_type=search_type),
                    self._view,
                    name="section_search_url"))
                self.add_to_sections_using_search(section_name)
        # create a urlpattern for the section_name
        urlpattern_last += url_patterns(
            '',
            url(r'^(?P<section_name>{section_name})/$'.format(section_name=section_name),
            self._view,
            name="section_url".format(section_name)))
        return urlpattern_first + urlpattern_last

    def get_appointment_tile(self):
        appointments = Appointment.objects.filter().order_by(appt_datetime__lt=datetime.datetime(date.today().year, date.today().month, date.today().day + 1))[0:10]
        return appointments

#    def get_action_items(self):
#        actions = ActionItem.objects.filter(action_status='open').order_by(action_datetime)[0:10]

# 1.5    def get(self, request, *args, **kwargs):
#            self._view(request, *args, **kwargs)

    def _view(self, request, *args, **kwargs):
        @login_required
        def view(request, *args, **kwargs):
            self.set_section_name(kwargs.get('section_name'))
            self.set_search_type(self.get_section_name(), kwargs.get('search_type'))
            search_result = None
            search_result_include_file = None
            if self.get_search_type(self.get_section_name()):
                search_cls = site_search.get(self.get_search_type(self.get_section_name()))
                search_instance = search_cls()
                search_result_include_file = search_instance.get_include_template_file()
                search_instance.prepare(request, **kwargs)
                page = request.GET.get('page', '1')
                if search_instance.form_is_valid:
                    search_result = search_instance.search(request, page)
                else:
                    search_result = search_instance.get_most_recent(page)
            return render_to_response(self.get_template(), {
                'app_name': settings.APP_NAME,
                'installed_apps': settings.INSTALLED_APPS,
                'selected_section': self.get_section_name(),
                'sections': self.get_section_list(),
                'section_name': self.get_section_name(),
                'search_name': self.get_search_name(self.get_section_name()),
                'sections_using_search': self.get_sections_using_search(),
                'search_type': self.get_search_type(self.get_section_name()),
                'add_model': self.get_add_model_cls(),
                'add_model_opts': self.get_add_model_opts(),
                'add_model_name': self.get_add_model_name(),
                'search_model_admin_url': 'url',
                'search_result': search_result,
                #'appointments': self.get_appointment_tile(),
                #'action_items': self.get_action_items_tile(),
                'search_result_include_file': search_result_include_file,
            }, context_instance=RequestContext(request))
        return view(request, *args, **kwargs)
