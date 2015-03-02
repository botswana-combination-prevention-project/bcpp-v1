from edc.base.form.forms import BaseModelForm

from ..models import SubjectDeath


class SubjectDeathForm (BaseModelForm):

    class Meta:
        model = SubjectDeath
