from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import date, timedelta, datetime
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from forms import LabForm, ResultForm, ResultItemForm, ReviewForm
from models import Lab, Result, ResultItem, Review, UpdateLog


class UpdateLogAdmin(MyModelAdmin): 
    list_display = ('subject_identifier', 'update_datetime')
    fields = ('subject_identifier', 'update_datetime')
    list_filter = ('update_datetime',)
    search_fields = ('subject_identifier',)
admin.site.register(UpdateLog, UpdateLogAdmin)

# Lab
class LabAdmin(MyModelAdmin): 

    form = LabForm

    list_display = ('subject_identifier', 'panel', "drawn_datetime", 'result_identifier',"release_datetime")
    
    list_filter = ('drawn_datetime','panel')

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
        "release_datetime"
    )

    radio_fields = {
        
    }

    filter_horizontal = (
        
    )

    """"""

admin.site.register(Lab, LabAdmin)

# Result
class ResultAdmin(MyModelAdmin): 

    form = ResultForm
    
    fields = (
        #"result_identifier",
        "result_datetime",
        "release_status",
        "release_datetime",
        "release_username",
        "comment",
        "dmis_result_guid",
        "lab"
    )

    radio_fields = {
        "release_status":admin.VERTICAL
    }

    filter_horizontal = (
        
    )

    """lab"""

admin.site.register(Result, ResultAdmin)

# ResultItem
class ResultItemAdmin(MyModelAdmin): 

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
        )
    
    list_filter = ('grade_flag', 'reference_flag',)    
    search_fields = ('test_code__code',)    

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
        "result"
    )

    radio_fields = {
        "result_item_quantifier":admin.VERTICAL,
        "validation_status":admin.VERTICAL
    }

    filter_horizontal = (
        
    )

    """testcode, result"""

admin.site.register(ResultItem, ResultItemAdmin)

# Review
class ReviewAdmin(MyModelAdmin): 

    form = ReviewForm

    fields = (
        "lab",
        "review_status",
        "review_datetime"
    )

    radio_fields = {
        "review_status":admin.VERTICAL
    }

    filter_horizontal = (
        
    )

    """lab"""

admin.site.register(Review, ReviewAdmin)
