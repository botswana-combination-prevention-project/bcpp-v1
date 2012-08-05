from django.contrib import admin
from bhp_export_data.actions import export_as_csv_action
from bhp_base_model.classes import BaseModelAdmin
from forms import LabForm, ResultForm, ResultItemForm, ReviewForm
from models import Lab, Result, ResultItem, Review, UpdateLog


class UpdateLogAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'update_datetime')
    fields = ('subject_identifier', 'update_datetime')
    list_filter = ('update_datetime',)
    search_fields = ('subject_identifier',)
admin.site.register(UpdateLog, UpdateLogAdmin)


class LabAdmin(BaseModelAdmin):
    form = LabForm
    list_display = ('subject_identifier', "receive_identifier", 'panel', "drawn_datetime", "release_status", 'result_identifier', "release_datetime")
    list_filter = ("release_status", 'drawn_datetime', "receive_datetime", 'panel')
    search_fields = ('subject_identifier', 'panel', 'receive_identifier', 'result_identifier')
    fields = (
        "subject_identifier",
        "release_status",
        "panel",
        "aliquot_identifier",
        "receive_datetime",
        "receive_identifier",
        "drawn_datetime",
        "order_identifier",
        "release_datetime")
admin.site.register(Lab, LabAdmin)


class ResultAdmin(BaseModelAdmin):
    form = ResultForm
    search_fields = ("result_identifier", "lab__subject_identifier", "lab__receive_identifier")
    list_display = (
        "result_identifier",
        "result_datetime",
        "release_status",
        "release_datetime",)
    fields = (
        "result_datetime",
        "release_status",
        "release_datetime",
        "release_username",
        "comment",
        "dmis_result_guid",
        "lab")
    radio_fields = {"release_status": admin.VERTICAL}
    list_filter = ("release_status", "result_datetime",)
admin.site.register(Result, ResultAdmin)


class ResultItemAdmin(BaseModelAdmin):

    form = ResultItemForm

    list_display = (
        "test_code",
        "result",
        "result_item_value",
        #"result_item_value_as_float",
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
    search_fields = ('test_code__code', 'result__result_identifier', "result__lab__subject_identifier", "result__lab__receive_identifier")

    fields = (
        "result_item_value",
        "result_item_quantifier",
        "result_item_datetime",
        "result_item_operator",
        "grade_range",
        "grade_flag",
        "reference_flag",
        "reference_range",
        "validation_status",
        "validation_datetime",
        "validation_username",
        "validation_reference",
        "comment",
        "error_code",
        "test_code",
        "result")
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
admin.site.register(ResultItem, ResultItemAdmin)


class ReviewAdmin(BaseModelAdmin):

    form = ReviewForm
    fields = (
        "review_status",
        "comment",
        "clinician_initials")
    radio_fields = {"review_status": admin.VERTICAL}
admin.site.register(Review, ReviewAdmin)
