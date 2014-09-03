from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import PlotLog, PlotLogEntry

from ..constants import INACCESSIBLE, CONFIRMED


class PlotLogForm(BaseModelForm):

    class Meta:
        model = PlotLog


class PlotLogEntryForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(PlotLogEntryForm, self).clean()
        try:
            plot_log_entry = PlotLogEntry.objects.get(plot_log=self.instance)
            plot_log_entry.allow_enrollment(plot_log_entry, exception_cls=forms.ValidationError)
        except PlotLogEntry.DoesNotExist:
            pass
        # confirm that an inaccessible log entry is not entered against a confirmed plot.
        plot = cleaned_data.get('plot_log').plot
        status = cleaned_data.get('log_status')
        if cleaned_data.get('rarely_present') == 'Yes' and cleaned_data.get('status') == 'PRESENT':
            raise forms.ValidationError('Members cannot be present and have the be rarely present.')
        if cleaned_data.get('rarely_present') == 'Yes' and cleaned_data.get('supervisor_vdc_confirm') == 'No':
            raise forms.ValidationError('There needs to be a confirmation from supervisor and VDC for a '
                                        'plot with rarely or seasonally present members.')
        if status == INACCESSIBLE and plot.action == CONFIRMED:
            raise forms.ValidationError('This plot has been \'confirmed\'. You cannot set it as INACCESSIBLE.')
        return cleaned_data

    class Meta:
        model = PlotLogEntry
