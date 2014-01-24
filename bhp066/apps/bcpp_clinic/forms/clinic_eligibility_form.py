from edc.base.form.forms import BaseModelForm
from ..models import ClinicEligibility


class ClinicEligibilityForm(BaseModelForm):

    class Meta:
        model = ClinicEligibility
