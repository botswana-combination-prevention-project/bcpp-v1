from edc.base.form.forms import BaseModelForm

from ..models import RepresentativeEligibility


class RepresentativeEligibilityForm(BaseModelForm):

    class Meta:
        model = RepresentativeEligibility
