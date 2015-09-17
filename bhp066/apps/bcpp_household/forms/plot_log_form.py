from datetime import datetime

from django import forms
from django.forms.util import ErrorList

from edc.base.form.forms import BaseModelForm

from ..constants import INACCESSIBLE, CONFIRMED, ACCESSIBLE
from ..models import PlotLog, PlotLogEntry


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

        if status == ACCESSIBLE:
            if cleaned_data.get('reason'):
                self._errors['reason'] = ErrorList([u'This field is not required.'])
                raise forms.ValidationError('Reason is not required if plot is accessible.')
            if cleaned_data.get('reason_other'):
                self._errors['reason_other'] = ErrorList([u'This field is not required.'])
                raise forms.ValidationError('Other reason is not required if plot is accessible.')
        if PlotLogEntry.objects.filter(
                created__year=datetime.today().year,
                created__month=datetime.today().month,
                created__day=datetime.today().day,
                plot_log__plot=plot_log.plot):
            if not self.instance.id:
                raise forms.ValidationError('The plot log entry has been added already.')

        return cleaned_data

    class Meta:
        model = PlotLogEntry
