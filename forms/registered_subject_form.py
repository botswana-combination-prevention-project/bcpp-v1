from bhp_registration.models import RegisteredSubject
from bhp_base_form.forms import BaseModelForm


class RegisteredSubjectForm (BaseModelForm):
    """Form for the RegisteredSubject model."""

    class Meta:
        model = RegisteredSubject
