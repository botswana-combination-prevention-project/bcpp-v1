from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from ..admin_site import bcpp_household_admin
from ..models import PlotLogEntry, PlotLog
from ..forms import PlotLogForm, PlotLogEntryForm

from .modeladmin_mixins import ModelAdminMixin


@admin.register(PlotLogEntry, site=bcpp_household_admin)
class PlotLogEntryAdmin(ModelAdminMixin):
    form = PlotLogEntryForm
    date_hierarchy = 'modified'
    fields = ('plot_log', 'report_datetime', 'log_status', 'reason', 'reason_other', 'comment')
    list_per_page = 15
    list_display = ('plot_log', 'log_status', 'report_datetime')
    list_filter = ('log_status', 'report_datetime', 'plot_log__plot__community', 'log_status')
    search_fields = ('log_status', 'plot_log__plot__community', 'plot_log__plot__plot_identifier')
    radio_fields = {
        'reason': admin.VERTICAL,
        'log_status': admin.VERTICAL
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "plot_log":
            if request.GET.get('plot_log'):
                kwargs["queryset"] = PlotLog.objects.filter(id__exact=request.GET.get('plot_log', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('plot_log')
                except ValueError:
                    self.readonly_fields.append('plot_log')
        return super(PlotLogEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def reponse_change_redirect_on_next_url(self, next_url_name, request, obj, post_url_continue,
                                            post_save, post_save_next, post_cancel):
        """Returns an http_response_redirect if next_url_name can be
        reversed otherwise None.

        Users may override to to add special handling for a named
        url next_url_name.

        .. note:: currently this assumes the next_url_name is reversible
                  using dashboard criteria or returns nothing.
        """
        custom_http_response_redirect = None
        if 'dashboard' in next_url_name:
            url = self.reverse_next_to_dashboard(next_url_name, request, obj)
            custom_http_response_redirect = HttpResponseRedirect(url)
            request.session['filtered'] = None
        else:
            kwargs = {}
            [kwargs.update({key: value}) for key, value in request.GET.iteritems() if key != 'next']
            url = next_url_name
            custom_http_response_redirect = HttpResponseRedirect(url)
            request.session['filtered'] = None
        return custom_http_response_redirect

    def reverse_next_to_dashboard(self, next_url_name, request, obj, **kwargs):
        url = ''
        if (next_url_name and request.GET.get('dashboard_id') and
                request.GET.get('dashboard_model') and request.GET.get('dashboard_type')):
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
            url = reverse('admin:{app_label}_{module_name}_{mode}'.format(
                app_label=app_label, module_name=module_name, mode=mode))
        else:
            url = next_url_name
        return url


class PlotLogEntryInline(admin.TabularInline):
    model = PlotLogEntry
    extra = 0
    max_num = 5


@admin.register(PlotLog, site=bcpp_household_admin)
class PlotLogAdmin(ModelAdminMixin):
    form = PlotLogForm
    instructions = []
    inlines = [PlotLogEntryInline, ]
    date_hierarchy = 'modified'
    list_per_page = 15
    list_display = ('plot', 'modified', 'user_modified', 'hostname_modified')
    readonly_fields = ('plot', )
    search_fields = ('plot__plot_identifier', 'plot__pk')
    list_filter = ('hostname_created', 'modified', 'user_modified')
