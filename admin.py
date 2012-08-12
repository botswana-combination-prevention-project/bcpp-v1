from django.contrib import admin
from bhp_export_data.actions import export_as_csv_action
from bhp_base_model.classes import BaseModelAdmin
from forms import ResultForm, ResultItemForm, ReviewForm
from models import Receive, Result, ResultItem, Review, UpdateLog, LisImportError, Order, Panel, TestCode
from actions import recalculate_grading


class ReceiveAdmin(BaseModelAdmin):
    list_display = ('registered_subject', "receive_identifier", "receive_datetime", 'created', 'modified')
    search_fields = ('registered_subject__subject_identifier', "receive_identifier",)

    def get_readonly_fields(self, request, obj):
        return [field.name for field in obj._meta.fields if field.editable and field.name not in ['requisition_identifier']]

admin.site.register(Receive, ReceiveAdmin)


class OrderAdmin(BaseModelAdmin):
    list_display = ("order_identifier", "subject_identifier", "panel", "order_datetime", 'created', 'modified')
    search_fields = ('aliquot__receive__registered_subject__subject_identifier', "order_identifier",)
    list_filter = ('status', 'panel__name')

    def get_readonly_fields(self, request, obj):
        return ['aliquot', 'panel', 'status', 'order_datetime', 'comment']
admin.site.register(Order, OrderAdmin)


class LisImportErrorAdmin(BaseModelAdmin):
    list_display = ('model_name', "identifier", "error_message")
    list_filter = ('model_name',)
    search_fields = ("identifier", "error_message")
admin.site.register(LisImportError, LisImportErrorAdmin)


class UpdateLogAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'update_datetime')
    fields = ('subject_identifier', 'update_datetime')
    list_filter = ('update_datetime',)
    search_fields = ('subject_identifier',)
admin.site.register(UpdateLog, UpdateLogAdmin)


class PanelAdmin(BaseModelAdmin):
    list_display = ('name', 'edc_name')
admin.site.register(Panel, PanelAdmin)


class TestCodeAdmin(BaseModelAdmin):
    list_display = ('code', 'name', 'edc_code', 'edc_name')
admin.site.register(TestCode, TestCodeAdmin)


class ResultAdmin(BaseModelAdmin):

    def __init__(self, *args, **kwargs):
        self.actions.append(recalculate_grading)
        super(ResultAdmin, self).__init__(*args, **kwargs)

    form = ResultForm
    search_fields = ("result_identifier", "order__aliquot__receive__registered_subject__subject_identifier", "order__aliquot__receive__receive_identifier")

    list_display = (
        "result_identifier",
        "subject_identifier",
        "result_datetime",
        "release_status",
        "release_datetime",)

    radio_fields = {"release_status": admin.VERTICAL}
    list_filter = ("release_status", "result_datetime",)

    def get_readonly_fields(self, request, obj):
        return [field.name for field in obj._meta.fields if field.editable]

admin.site.register(Result, ResultAdmin)


class ResultItemAdmin(BaseModelAdmin):

    form = ResultItemForm

    list_display = (
        "test_code",
        "result",
        "result_item_value",
        "result_item_quantifier",
        "result_item_datetime",
        "result_item_operator",
        "grade_range",
        "grade_flag",
        "reference_flag",
        "reference_range",
        "created",
        "modified",
        )

    list_filter = ('grade_flag', 'reference_flag', "result_item_datetime", "test_code", "created", "modified")
    search_fields = ('test_code__code', 'result__result_identifier',
                     "result__order__aliquot__receive__registered_subject__subject_identifier",
                     "result__order__aliquot__receive__receive_identifier")
    radio_fields = {
        "result_item_quantifier": admin.VERTICAL,
        "validation_status": admin.VERTICAL}
    actions = [export_as_csv_action("CSV Export: ...with basic demographics",
        fields=[],
        exclude=['id', ],
        extra_fields=[
            {'subject_identifier': 'result__lab__subject_identifier'},
            {'gender': 'result__lab__gender'},
            {'dob': 'result__lab__dob'},
            ]), ]

    def get_readonly_fields(self, request, obj):
        return [field.name for field in obj._meta.fields if field.editable]

admin.site.register(ResultItem, ResultItemAdmin)


class ReviewAdmin(BaseModelAdmin):

    form = ReviewForm

    radio_fields = {"review_status": admin.VERTICAL}
admin.site.register(Review, ReviewAdmin)
