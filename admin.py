from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from lab_aliquot.models import Aliquot


class ReceiveAutocomplete(AutocompleteSettings):
    search_fields = ('^receive_identifier',)


class AliquotTypeAutocomplete(AutocompleteSettings):

    search_fields = ('^numeric_code', '^alpha_code', '^name',)

autocomplete.register(Aliquot.receive, ReceiveAutocomplete)
autocomplete.register(Aliquot.aliquot_type, AliquotTypeAutocomplete)


class AliquotAdmin(AutocompleteAdmin, BaseModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.aliquot_identifier = self.model.objects.get_identifier(
                parent_identifier=request.POST.get('parent_identifier'),
                aliquot_type=request.POST.get('aliquot_type'),
                )
        save = super(AliquotAdmin, self).save_model(request, obj, form, change)
        return save

    def get_readonly_fields(self, request, obj=None):
        if obj:  # In edit mode
            return ('aliquot_type', 'receive', 'original_measure',) + self.readonly_fields
        else:
            return self.readonly_fields
    fields = ('aliquot_identifier', 'receive', 'aliquot_type', 'medium', 'original_measure',
              'current_measure', 'measure_units', 'aliquot_condition', 'status', 'comment')
    list_display = ('aliquot_identifier', 'aliquot_type', 'original_measure', 'current_measure',
                    'measure_units', 'aliquot_condition', 'receive')
    readonly_fields = ('aliquot_identifier',)
admin.site.register(Aliquot, AliquotAdmin)
