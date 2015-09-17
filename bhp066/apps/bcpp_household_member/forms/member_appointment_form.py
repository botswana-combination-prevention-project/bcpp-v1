from edc.base.form.forms import BaseModelForm

from ..models import MemberAppointment


class MemberAppointmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(MemberAppointmentForm, self).clean()
        return cleaned_data

    class Meta:
        model = MemberAppointment
