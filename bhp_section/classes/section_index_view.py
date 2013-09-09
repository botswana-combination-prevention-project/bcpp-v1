from django.conf.urls.defaults import patterns as url_patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from base_section_index_view import BaseSectionIndexView


class SectionIndexView(BaseSectionIndexView):

    app_name = 'bhp_section'

    def get_default_sections(self):
        return []

    def urlpatterns(self, view=None):
        """ Generates a urlpattern for the view of this subclass."""
        if view is None:
            view = self._view
        urlpattern = []
        for section_name in self.get_section_name_list():
            urlpattern += url_patterns(
                '{app_name}.views'.format(app_name=self.app_name),
                url(r'^(?P<selected_section>{section_name})/$'.format(section_name=section_name),
                view,
                name="section_index_url".format(section_name=section_name)))
        urlpattern += url_patterns(
                '{app_name}.views'.format(app_name=self.app_name),
                url(r'',
                view,
                name="section_index_url"))
        return urlpattern

    def _view(self, request, *args, **kwargs):
        @login_required
        def view(request, *args, **kwargs):
            """Renders the view."""
            self.selected_section = kwargs.get('selected_section')
            return render_to_response(
                      'section_index.html',
                      {'sections': self.get_section_list(),
                       'selected_section': self.selected_section},
                      context_instance=RequestContext(request))
        return view(request, *args, **kwargs)

section_index_view = SectionIndexView()
