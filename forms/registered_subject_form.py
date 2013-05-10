from bhp_registration.models import RegisteredSubject
from bhp_base_form.forms import BaseModelForm


class RegisteredSubjectForm (BaseModelForm):

    class Meta:
        model = RegisteredSubject
