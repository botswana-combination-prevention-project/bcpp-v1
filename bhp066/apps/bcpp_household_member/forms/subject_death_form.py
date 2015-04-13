from edc.subject.adverse_event.forms import BaseInfantDeathForm

from ..models import SubjectDeath


class SubjectDeathForm (BaseInfantDeathForm):

    class Meta:
        model = SubjectDeath
