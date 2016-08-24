import re

from django.db.models import Q


class ModifyFormLabelMixin:
    """Replace a from label datetime placeholder with a datetime value.

    Keyword arguments:
    QUERY_MODEL_PARAMETERS -- the dictionary for querying criteria.
    """
    # QUERY_MODEL_PARAMETERS = {"field_name_to_modify_lable": [query_model, "replacement_model_field_attribute", "foreinkey_model", "foreign_key_field_attribute", "query_model_field_attribute"]}
    QUERY_MODEL_PARAMETERS = {}

    def get_form_post(self, form, request, obj, **kwargs):
        return self.replace_labels(form, request)

    def replace_labels(self, form, request):
        WIDGET = 1
        model_obj = None
        foreign_key_instance = None
        for _, fld in enumerate(form.base_fields.items()):
            for key, value in self.QUERY_MODEL_PARAMETERS.iteritems():
                try:
                    foreign_key_instance = self.QUERY_MODEL_PARAMETERS[key][2].objects.get(pk=request.GET.get(self.QUERY_MODEL_PARAMETERS[key][3]))
                except self.QUERY_MODEL_PARAMETERS[key][2].DoesNotExist:
                    pass
                try:
                    model_obj = self.QUERY_MODEL_PARAMETERS[key][0].objects.get(Q(**{self.QUERY_MODEL_PARAMETERS[key][4]: getattr(foreign_key_instance, self.QUERY_MODEL_PARAMETERS[key][4])}))
                except self.QUERY_MODEL_PARAMETERS[key][0].DoesNotExist:
                    pass
                if model_obj:
                    obj_datetime = getattr(model_obj, value[1]).strftime('%A, %B %d, %Y at %H:%M hours')
                    if key == fld[0]:
                        if not re.match(r'^\d+\.', str(fld[WIDGET].label)) and re.search(r"\[\]", str(fld[WIDGET].label)):
                            fld[WIDGET].label = re.sub("\[\]", obj_datetime, fld[WIDGET].label)
        return form
