from bhp_base_form.classes import BaseModelForm
from bhp_data_manager.models import ActionItem
from bhp_registration.models import RegisteredSubject


class ActionItemForm(BaseModelForm):

    class Meta:
        model = ActionItem
