from django.contrib import admin

from ..forms import NonPregnancyForm
from ..models import NonPregnancy

from .subject_visit_model_admin import SubjectVisitModelAdmin


class NonPregnancyAdmin(SubjectVisitModelAdmin):

    form = NonPregnancyForm
    fields = (
        "subject_visit",
        'more_children',
    )
    radio_fields = {"more_children": admin.VERTICAL}
admin.site.register(NonPregnancy, NonPregnancyAdmin)
