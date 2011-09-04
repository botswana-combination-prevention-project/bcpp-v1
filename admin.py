from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import date, timedelta, datetime
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from forms import LocalResultForm, LocalResultItemForm, ReviewForm
from models import LocalResult, LocalResultItem, Review


# LocalResult
class LocalResultAdmin(MyModelAdmin): 

    form = LocalResultForm

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

admin.site.register(LocalResult, LocalResultAdmin)

# LocalResultItem
class LocalResultItemAdmin(MyModelAdmin): 

    form = LocalResultItemForm

    fields = (
        "test_code",
        "result_item_value",
        "result_item_quantifier",
        "result_item_datetime",
        "result_item_operator",
        "validation_status",
        "validation_datetime",
        "validation_username",
        "validation_reference",
        "comment",
        "error_code",
        "local_result"
    )

    radio_fields = {
        "result_item_quantifier":admin.VERTICAL,
        "validation_status":admin.VERTICAL
    }

    filter_horizontal = (
        
    )

    """testcode, localresult"""

admin.site.register(LocalResultItem, LocalResultItemAdmin)

# Review
class ReviewAdmin(MyModelAdmin): 

    form = ReviewForm

    fields = (
        "local_result",
        "review_status",
        "review_datetime"
    )

    radio_fields = {
        "review_status":admin.VERTICAL
    }

    filter_horizontal = (
        
    )

    """localresult"""

admin.site.register(Review, ReviewAdmin)
