from datetime import datetime, date
from django.conf.urls.defaults import patterns as url_patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from section_index import section_index
from bhp_appointment.models import Appointment
from bhp_data_manager.models import ActionItem
from bhp_search.classes import search
from bhp_section.exceptions import SectionError


class Section(object):

    def __init__(self):
        self._template = None
        self._section_name = None
        self.search_label = None
        self.urlpattern_prepared = False
        self._sections_using_search = []
        self._custom_template = {}

    def _get_custom_template(self, section_name=None):
        return self._custom_template.get(section_name, self.get_default_template())

    def set_section_name(self, value=None):
        self._section_name = value
        #self._set_template()

    def get_section_name(self):
        if not self._section_name:
            self.set_section_name()
        return self._section_name

    def get_sections_using_search(self, section_name=None):
        if not self.urlpattern_prepared:
            raise SectionError('Call urlpatterns(), in urls.py, first to update the list for those sections linked to a search class')
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
        elif self._get_custom_template(self.get_section_name()):
            self._template = self._get_custom_template(self.get_section_name())
        else:
            self._template = self.get_default_template()

    def get_default_template(self):
            if self.get_sections_using_search(self.get_section_name()):
                #return 'section_using_search.html'
                return 'subject_section.html'

            else:
                return 'section.html'

    def get_template(self):
        if not self._template:
            self._set_template()
        return self._template

    def urlpatterns(self, view=None):
        """ Generates a urlpattern for the view of this subclass."""
        self.urlpattern_prepared = True
        if view is None:
            view = self._view
        urlpattern_first = []
        urlpattern_last = []
        for section_name in section_index.get_section_name_list():
            # try to match this section to a search class
            for search_label in search.get_registry():
                # if search classes registered, create urls for the search classes for current section_name
                if search.get_registry(search_label)().validate_section_name(section_name):
                    urlpattern_first += url_patterns(
                        '',
                        url(r'^(?P<section_name>{section_name})/(?P<search_label>{search_label})/$'.format(section_name=section_name, search_label=search_label),
                        self._view,
                        name="section_search_url".format(section_name)))
                    self.add_to_sections_using_search(section_name)
            # create a urlpattern for each section_name
            urlpattern_last += url_patterns(
                '',
                url(r'^(?P<section_name>{section_name})/$'.format(section_name=section_name),
                self._view,
                name="section_url".format(section_name)))
        return urlpattern_first + urlpattern_last

    def get_appointment_tile(self):
        appointments = Appointment.objects.filter().order_by(appt_datetime__lt=datetime.datetime(date.today().year, date.today().month, date.today().day + 1))[0:10]
        return appointments

    def get_action_items(self):
        actions = ActionItem.objects.filter(action_status='open').order_by(action_datetime)[0:10]

    def _view(self, request, **kwargs):
        self.set_section_name(kwargs.get('section_name'))
        self.search_label = kwargs.get('search_label')
        search_results = None
        top_result_include_file = None
        if self.search_label:
            top_result_include_file = "{0}_include.html".format(self.search_label)
            search_cls = search.get('word')
            search_instance = search_cls()
            search_instance.prepare(request, **kwargs)
            if search_instance.form_is_valid:
                search_instance.search(request)
            if not self.search_label:
                self.search_label = search_instance.get_search_label()
            page = request.GET.get('page', '1')
            search_results = search_instance.get_most_recent(self.search_label, page)
        return render_to_response(self.get_template(), {
            'app_name': settings.APP_NAME,
            'selected_section': self.get_section_name(),
            'sections': section_index.get_section_list(),
            'section_name': self.get_section_name(),
            'sections_using_search': self.get_sections_using_search(),
            'search_label': self.search_label,
            'add_search_model_label': 'Add',
            'search_model_admin_url': 'url',
            'search_model_next_url_name'
            'search_result': search_results,
            'appointments': self.get_appointment_tile(),
            'action_items': self.get_action_items_tile(),
            'top_result_include_file': top_result_include_file,
        }, context_instance=RequestContext(request))

section = Section()
