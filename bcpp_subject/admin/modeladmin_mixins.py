from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin)

from ..models import SubjectVisit


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin, ModelAdminAuditFieldsMixin,
                      ModelAdminReadOnlyMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')


class CrfModelAdminMixin(ModelAdminMixin):

    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subject_visit' and request.GET.get('subject_visit'):
            kwargs["queryset"] = SubjectVisit.objects.filter(pk=request.GET.get('subject_visit', 0))
        return super(CrfModelAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)
