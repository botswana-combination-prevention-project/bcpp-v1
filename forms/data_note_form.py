from bhp_base_form.classes import BaseModelForm
from bhp_data_manager.models import DataNote
from bhp_registration.models import RegisteredSubject


class DataNoteForm(BaseModelForm):

#     def __init__(self, *args, **kwargs):
#         super(DataNoteForm, self).__init__(*args, **kwargs)
#         if self.instance.registered_subject:
#             self.fields['registered_subject'].queryset = RegisteredSubject.objects.filter(pk=self.instance.registered_subject.pk)

    class Meta:
        model = DataNote
