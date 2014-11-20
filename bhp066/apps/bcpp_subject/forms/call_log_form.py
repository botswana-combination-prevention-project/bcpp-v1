from edc.base.form.forms import BaseModelForm

from ..models import CallLog, CallLogEntry


class CallLogForm (BaseModelForm):

    class Meta:
        model = CallLog


class CallLogEntryForm (BaseModelForm):

    class Meta:
        model = CallLogEntry
