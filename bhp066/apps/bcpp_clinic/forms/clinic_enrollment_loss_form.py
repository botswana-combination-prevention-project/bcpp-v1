from ..models import ClinicEnrollmentLoss

from edc.base.form.forms import BaseModelForm


class ClinicEnrollmentLossForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicEnrollmentLossForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicEnrollmentLoss
