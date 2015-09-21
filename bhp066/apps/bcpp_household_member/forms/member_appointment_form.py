from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import MemberAppointment


class MemberAppointmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(MemberAppointmentForm, self).clean()
        return cleaned_data

    class Meta:
        model = MemberAppointment
