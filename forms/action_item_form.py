from bhp_base_form.classes import BaseModelForm
from bhp_data_manager.models import ActionItem


class ActionItemForm(BaseModelForm):

    class Meta:
        model = ActionItem
