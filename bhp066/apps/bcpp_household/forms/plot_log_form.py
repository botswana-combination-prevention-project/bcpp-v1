from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import PlotLog, PlotLogEntry


class PlotLogForm(BaseModelForm):

    class Meta:
        model = PlotLog


class PlotLogEntryForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(PlotLogEntryForm, self).clean()
        try:
            plot_log_entry = PlotLogEntry.objects.get(plot_log=self.instance)
        except:
            plot_log_entry = None
        if plot_log_entry:
            plot_log_entry.allow_enrollement(plot_log_entry, PlotLogEntry(**cleaned_data), exception_cls=forms.ValidationError)
        # confirm that an inaccessible log entry is not entered against a confirmed plot.
        plot = cleaned_data.get('plot_log').plot
        status = cleaned_data.get('log_status')
        if cleaned_data.get('rarely_present') == 'Yes' and cleaned_data.get('status') == 'PRESENT':
            raise forms.ValidationError('Members cannot be present and have the be rarely present.')
        if cleaned_data.get('rarely_present') == 'Yes' and cleaned_data.get('supervisor_vdc_confirm') == 'No':
            raise forms.ValidationError('There needs to be confirmation from supervisor and VDC for rarely or seasonal members.')
        if status == 'INACCESSIBLE' and plot.action == 'confirmed':
            raise forms.ValidationError('This plot has been confirmed. You cannot set it as INACCESSIBLE.')
        return cleaned_data
    class Meta:
        model = PlotLogEntry
