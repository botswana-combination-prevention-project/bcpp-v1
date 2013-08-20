from django.contrib import admin
from bcpp_subject.admin.subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_htc.models import FollowupContactPermission
from bcpp_htc.forms import FollowupContactPermissionForm


class FollowupContactPermissionAdmin(SubjectVisitModelAdmin):

    form = FollowupContactPermissionForm

    fields = (
      "contact_permission",
      "contact_family",
      "male_contact", 
      "male_family",
      "pregnant_permission",
    )
    radio_fields = {
        "contact_permission": admin.VERTICAL,
        "contact_family": admin.VERTICAL,
        "male_contact": admin.VERTICAL,
        "male_family": admin.VERTICAL,   
        "pregnant_permission": admin.VERTICAL,   
        }
    instructions = [("For newly identified HIV positive individuals"
                     " and known HIV positive individuals not enrolled"
                     " in care, ask questions 37 and 37a.")]

admin.site.register(FollowupContactPermission, FollowupContactPermissionAdmin)
