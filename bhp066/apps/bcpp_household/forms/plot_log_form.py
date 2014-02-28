from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import PlotLog, PlotLogEntry


class PlotLogForm(BaseModelForm):

    class Meta:
        model = PlotLog


class PlotLogEntryForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(PlotLogEntryForm, self).clean()
        # confirm that an inaccessible log entry is not entered against a confirmed plot.
        plot = cleaned_data.get('plot_log').plot
        status = cleaned_data.get('log_status')
        if status == 'INACCESSIBLE' and plot.action != 'unconfirmed':
            raise forms.ValidationError('This plot has been confirmed. You cannot set it as INACCESSIBLE.')
        return cleaned_data

    class Meta:
        model = PlotLogEntry
