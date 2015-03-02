from django import forms
from datetime import datetime, timedelta

from edc.base.form.forms import BaseModelForm

from ..models import PlotLog, PlotLogEntry

from ..constants import INACCESSIBLE, CONFIRMED


class PlotLogForm(BaseModelForm):

    class Meta:
        model = PlotLog


class PlotLogEntryForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(PlotLogEntryForm, self).clean()
        plot_log = cleaned_data.get('plot_log')
        plot_log.plot.allow_enrollment('default',
                                       plot_instance=plot_log.plot,
                                       exception_cls=forms.ValidationError)
        # confirm that an inaccessible log entry is not entered against a confirmed plot.
        status = cleaned_data.get('log_status')
        if cleaned_data.get('rarely_present') == 'Yes' and cleaned_data.get('status') == 'PRESENT':
            raise forms.ValidationError('Members cannot be present and have the be rarely present.')
        if cleaned_data.get('rarely_present') == 'Yes' and cleaned_data.get('supervisor_vdc_confirm') == 'No':
            raise forms.ValidationError('There needs to be a confirmation from supervisor and VDC for a '
                                        'plot with rarely or seasonally present members.')
        if status == INACCESSIBLE and plot_log.plot.action == CONFIRMED:
            raise forms.ValidationError('This plot has been \'confirmed\'. You cannot set it as INACCESSIBLE.')

        if PlotLogEntry.objects.filter(
                            created__range=(datetime.today() + timedelta(days=-1),
                                                       datetime.today() + timedelta(days=1))
                                                                , plot_log__plot=plot_log.plot):
            if not self.instance.id:
                raise forms.ValidationError('The plot log entry has been added already.')

        return cleaned_data

    class Meta:
        model = PlotLogEntry
