from django.conf.urls.defaults import patterns as url_patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from base_section import BaseSection


class SectionIndex(BaseSection):

    app_name = 'bhp_section'

    def get_default_sections(self):
        return [('appointments', 'Appointments', 100), ('labs', 'Labs', 110), ('statistics', 'Statistics', 120), ('audit_trail', 'Audit', 130), ('administration', 'Administration', 140)]

    def urlpatterns(self, view=None):
        """ Generates a urlpattern for the view of this subclass."""
        if view is None:
            view = self.view
        urlpattern = []
        #for section_name in self.get_section_name_list():
        #    urlpattern += url_patterns(
        #        '{app_name}.views'.format(app_name=self.app_name),
        #        url(r'^(?P<selected_section>{section_name})/$'.format(section_name=section_name),
        #        self.view,
        #        name="section_index_{0}_url".format(section_name)))
        urlpattern += url_patterns(
                '{app_name}.views'.format(app_name=self.app_name),
                url(r'',
                self.view,
                name="section_index_url"))
        return urlpattern

    #@login_required
    def view(self, request, **kwargs):
        """Renders the view."""
        self.selected_section = kwargs.get('selected_section')
        return render_to_response(
                  'section_index.html',
                  {'sections': self.get_section_list(),
                   'selected_section': self.selected_section},
                  context_instance=RequestContext(request))

section_index = SectionIndex()
