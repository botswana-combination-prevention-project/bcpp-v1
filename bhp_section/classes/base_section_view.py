import re
from datetime import datetime, date
#from django.views.base import View  # for 1.5
from django.conf.urls.defaults import patterns, url
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bhp_appointment.models import Appointment
from bhp_search.classes import site_search
from bhp_section.exceptions import SectionError


# class Section(View):  # 1.5
class BaseSectionView(object):

    section_name = None
    section_display_name = None
    section_display_index = None
    section_list = None
    section_template = None
    add_model = None

    def __init__(self):
        self._context = {}
        self._template = None
        self._section_name = None
        self._section_display_name = None
        self._section_display_index = None
        self._add_model_cls = None
        self._section_list = None
        self._sections_using_search = []
        self._custom_template = {}
        self._search_type = {}
        self._search_name = {}

    @property
    def context(self):
        """Returns the template context."""
        return self._context

    def update_context(self, **kwargs):
        """Updates the template context."""
        for k, v in kwargs.iteritems():
            self._context[k] = v

    def set_section_list(self, value=None):
        """Sets the section list."""
        if self.section_list:
            # class variable set in urls
            self._section_list = self.section_list
        elif not value:
            raise AttributeError('Attribute \'sections_list\' may not be None. Should be set in urls.py')
        else:
            self._section_list = value

    def get_section_list(self):
        """Returns the section list."""
        if not self._section_list:
            self.set_section_list()
        return self._section_list

    def set_section_name(self, value=None):
        """Sets the name for this section."""
        if self.section_name:  # try for class attribute first
            self._section_name = self.section_name
        else:
            self._section_name = value
        self._set_template()

    def get_section_name(self):
        """Returns the name for this section."""
        if not self._section_name:
            self.set_section_name()
        return self._section_name

    def set_section_display_name(self, value=None):
        """Sets the name for this section."""
        if self.section_display_name:  # try for class attribute first
            self._section_display_name = self.section_display_name
        else:
            self._section_display_name = value

    def get_section_display_name(self):
        """Returns the name for this section."""
        if not self._section_display_name:
            self.set_section_display_name()
        return self._section_display_name

    def set_section_display_index(self, value=None):
        """Sets the name for this section."""
        if self.section_display_index:  # try for class attribute first
            self._section_display_index = self.section_display_index
        else:
            self._section_display_index = value

    def get_section_display_index(self):
        """Returns the name for this section."""
        if not self._section_display_index:
            self.set_section_display_index()
        return self._section_display_index

    def _set_add_model_cls(self, value=None):
        """Sets the model class used for the 'Add' button."""
        if self.add_model:  # try for class attribute first
            self._add_model_cls = self.add_model
        else:
            self._add_model_cls = value

    def get_add_model_cls(self):
        """Returns the 'Add' model class."""
        if not self._add_model_cls:
            self._set_add_model_cls()
        return self._add_model_cls

    def get_add_model_name(self):
        """Returns the name of the 'Add' model class."""
        if self.get_add_model_cls():
            return self.get_add_model_cls()._meta.verbose_name
        return None

    def get_add_model_opts(self):
        """Returns the model Meta class options."""
        if self.get_add_model_cls():
            return self.get_add_model_cls()._meta
        return None

    def set_search_type(self, section_name, search_type=None):
        """Sets the search type.

        Called from url_patterns()

        If the `section name` is listed as a search type, the :func:`view` method
        will get the search class from the `site_search` global and try to search against
        the search class' search model."""
        if search_type:
            self._search_type.update({section_name: search_type})

    def get_search_type(self, section_name=None):
        """Returns the search type for this section."""
        if not section_name:
            section_name = self.get_section_name()
        if not section_name in self._search_type:
            self.set_search_type(section_name)
        if section_name in self._search_type:
            return self._search_type.get(section_name)
        return None

    def set_search_name(self, section_name, search_name=None):
        """Sets the search name to associate a search class with this section.
        """
        if search_name:
            self._search_name.update({section_name: search_name})

    def get_search_name(self, section_name):
        """Returns the search name."""
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
        """Sets the template for this section."""
        if template:
            self._template = template
        elif self.section_template:
            self._template = self.section_template
        else:
            self._template = self._get_default_template()

    def get_template(self):
        """Returns the template set for this section."""
        if not self._template:
            self._set_template()
        return self._template

    def _get_default_template(self):
        return 'section_{0}.html'.format(self.get_section_name())

    def urlpatterns(self, view=None):
        """ Generates urlpatterns for the view of this section.

        If this section is associated with a search class registered with `site_search` global, patterns for search
        will also be generated."""
        if not site_search.is_autodiscovered:
            raise SectionError('Search register not ready. Call search.autodiscover() first.')
        if view is None:
            view = self._view
        urlpattern_first = []
        urlpattern_last = []
        section_name = self.get_section_name()
        for search_type, search_cls in site_search.get_registry().iteritems():
            # for each type of search, look for an association with this section_name
            if search_cls().get_section_name() == section_name:
                self.set_search_type(section_name, search_type)
                self.set_search_name(section_name, search_cls().name)
                urlpattern_first += patterns(
                    '',
                    url(re.compile('^(?P<section_name>{section_name})/(?P<search_type>{search_type})/(?P<search_term>[A-Za-z0-9\-]+)/$'.format(section_name=section_name, search_type=search_type)),
                        self._view,
                        name="section_search_url"),
                    url(r'^(?P<section_name>{section_name})/(?P<search_type>{search_type})/$'.format(section_name=section_name, search_type=search_type),
                        self._view,
                        name="section_search_url"))
                self.add_to_sections_using_search(section_name)
        # create a urlpattern for the section_name
        urlpattern_last += patterns(
            '',
            url(r'^(?P<section_name>{section_name})/(?P<search_term>[A-Za-z0-9\-\[\]]+)/$'.format(section_name=section_name),
                self._view,
                name="section_url"),
            url(r'^(?P<section_name>{section_name})/$'.format(section_name=section_name),
                self._view,
                name="section_url"))
        return urlpattern_first + urlpattern_last

    def get_appointment_tile(self):
        """Not used."""
        appointments = Appointment.objects.filter().order_by(appt_datetime__lt=datetime.datetime(date.today().year, date.today().month, date.today().day + 1))[0:10]
        return appointments

#    def get_action_items(self):
#        actions = ActionItem.objects.filter(action_status='open').order_by(action_datetime)[0:10]
# 1.5    def get(self, request, *args, **kwargs):
#            self._view(request, *args, **kwargs)

    def _contribute_to_context(self, context, request, *args, **kwargs):
        """Wraps :func:`contribute_to_context`."""
        context = self.contribute_to_context(context, request, *args, **kwargs)
        return context

    def contribute_to_context(self, context, request, *args, **kwargs):
        """Users may override to update the template context with {key, value} pairs."""
        return context

    def _get_search_result_include_template(self):
        """Wraps the user method :func:`get_search_result_include_template` and
        returns the template that displays the section\'s search_result.

        If there is no search class for the section, returns None"""
        template = self.get_search_result_include_template()
        if not template:
            # return a default template, if there is a search class for this section
            search_cls = site_search.get(self.get_search_type(self.get_section_name()))
            if search_cls:
                template = search_cls().get_search_result_include_template()
        return template

    def get_search_result_include_template(self):
        """Returns the template that displays the section\'s search_result.

        Users may override"""
        return None

    def _get_search_result(self, request, **kwargs):
        """Wraps the user method :func:`get_search_result` to return a search result or calls the default method :func:`get_default_search_result`."""
        search_result = self.get_search_result(request, **kwargs)
        if not search_result:
            search_result = self.get_default_search_result(request, **kwargs)
        return search_result

    def get_search_result(self, request, **kwargs):
        """Users may override to return an iterable search result."""
        return []

    def get_default_search_result(self, request, **kwargs):
        """Returns a default search result if :func:`get_search_result` returns None."""
        search_result = None
        if self.get_search_type(self.get_section_name()):
            searcher_cls = site_search.get(self.get_search_type(self.get_section_name()))
            searcher = searcher_cls()
            searcher.prepare(request, **kwargs)
            page = request.GET.get('page', '1')
            if searcher.form_is_valid:
                search_result = searcher.search(request, page)
            if not search_result:
                search_result = searcher.get_most_recent(page)
        return search_result

    def _paginate(self, search_result, page=1, results_per_page=None):
        """Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        Keyword Arguments:
            results_per_page: (default: 25)
        """
        if not results_per_page:
            results_per_page = 25
        if search_result:
            paginator = Paginator(search_result, results_per_page)
            try:
                search_result = paginator.page(page)
            except (EmptyPage, InvalidPage):
                search_result = paginator.page(paginator.num_pages)
        return search_result

    def view(self, request, *args, **kwargs):
        """Default view for this section called by :func:`_view`.

        .. note:: Instead of overriding, try adding to the context using :func:`contribute_to_context`.

        Default context includes::
            * app_name: settings.APP_NAME,
            * installed_apps: settings.INSTALLED_APPS,
            * selected_section: from :func:`get_section_name`,
            * sections: from :func:`get_section_list`,
            * section_name: from :func:`get_section_name`,
            * search_name: from :func:`get_search_name` for this section name,
            * sections_using_search: from :func:`get_sections_using_search`,
            * search_type: from :func:`get_search_type` for this section name,
            * add_model: from :func:`get_add_model_cls`,
            * add_model_opts: from :func:`get_add_model_opts`,
            * add_model_name: from :func:`get_add_model_name`,
            * search_model_admin_url: 'url',
            * search_result: search_result,
            * search_result_include_file: search_result_include_file,
        """
        self.set_section_name(kwargs.get('section_name'))
        search_term = kwargs.get('search_term', '')
        #page = kwargs.get('page', 1)
        page = request.GET.get('page')
        if request.method == 'POST':
            page = 1
        default_context = {
            'app_name': settings.APP_NAME,
            'installed_apps': settings.INSTALLED_APPS,
            'selected_section': self.get_section_name(),
            'sections': self.get_section_list(),
            'section_name': self.get_section_name(),
            'search_name': self.get_search_name(self.get_section_name()),
            'search_term': search_term,
            'sections_using_search': self.get_sections_using_search(),
            'search_type': self.get_search_type(self.get_section_name()),
            'add_model': self.get_add_model_cls(),
            'add_model_opts': self.get_add_model_opts(),
            'add_model_name': self.get_add_model_name(),
            'search_model_admin_url': 'url',
            'search_result': self._paginate(self._get_search_result(request, **kwargs), page),
            'search_result_include_file': self._get_search_result_include_template(),
            }
        # add extra values to the context dictionary
        context = self._contribute_to_context(default_context, request, **kwargs)
        return render_to_response(self.get_template(), context, context_instance=RequestContext(request))

    def _view(self, request, *args, **kwargs):
        """Wraps :func:`view` method to force login and treat this like a class based view."""
        @login_required
        def view(request, *args, **kwargs):
            return self.view(request, *args, **kwargs)
        return view(request, *args, **kwargs)
