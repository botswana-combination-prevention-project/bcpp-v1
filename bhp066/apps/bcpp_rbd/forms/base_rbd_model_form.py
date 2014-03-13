from edc.subject.consent.forms import BaseConsentedModelForm

from ..models import RBDVisit


class BaseRBDModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseRBDModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['rbd_visit'].queryset = RBDVisit.objects.filter(pk=self.instance.rbd_visit.pk)
        except:
            pass
