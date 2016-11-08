from django.core.urlresolvers import reverse
from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin

from bhp066.apps.bcpp_survey.models import Survey

from ..constants import ANNUAL, ANNUAL_CODES
from ..models import SubjectVisit
from edc.subject.appointment.models.appointment import Appointment


class SubjectVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the subject visit model."""

    visit_model = SubjectVisit
    visit_attr = 'subject_visit'
    dashboard_type = 'subject'
    date_heirarchy = 'subject_visit__report_datetime'
    current_survey = Survey.objects.current_survey().survey_slug
    first_survey = Survey.objects.first_survey.survey_slug

    def __init__(self, *args, **kwargs):
        self.subject_visit = None
        self.obj_instance = None
        lookups = []
        super(BaseVisitTrackingModelAdmin, self).__init__(*args, **kwargs)
        self.list_filter = list(self.list_filter)
        try:
            self.list_filter.remove('subject_visit')
        except ValueError:
            pass
        self.list_filter.extend(['created', 'modified', 'hostname_created', 'hostname_modified'])
        self.list_filter = list(set(self.list_filter))
        self.search_fields = list(self.search_fields)
        if self.visit_model:
            lookups = ['{}__appointment__registered_subject__identity'.format(self.visit_attr)]
            lookups.append('{}__appointment__registered_subject__first_name'.format(self.visit_attr))
            lookups.append('{}__subject_identifier'.format(self.visit_attr))
        lookups.append('id')
        for lookup in lookups:
            try:
                self.search_fields.index(lookup)
            except ValueError:
                self.search_fields.insert(0, lookup)

    def edc_readonly_next(self, dashboard_id):
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'dashboard_type': 'subject',
                'dashboard_model': 'visit',
                'dashboard_id': dashboard_id,
                'show': 'forms'
            })
        return url

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        dashboard_id = request.GET.get('dashboard_id')
        if request.GET.get('edc_readonly'):
            extra_context.update({'edc_readonly': request.GET.get('edc_readonly')})
            extra_context.update({'edc_readonly_next': self.edc_readonly_next(dashboard_id)})
        return super(SubjectVisitModelAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def get_form_post(self, form, request, obj, **kwargs):
        NAME = 0
        WIDGET = 1
        form = super(SubjectVisitModelAdmin, self).get_form_post(form, request, obj, **kwargs)
        if form.optional_attrs:
            try:
                self.subject_visit = SubjectVisit.objects.get(pk=request.GET.get('subject_visit'))
                if self.subject_visit.appointment.visit_definition.code in ANNUAL_CODES:
                    for fld in form.base_fields.iteritems():
                        try:
                            fld[WIDGET].label = form.optional_attrs[ANNUAL]['label'][fld[NAME]]
                        except KeyError:
                            pass
                        try:
                            fld[WIDGET].help_text = form.optional_attrs[ANNUAL]['help_text'][fld[NAME]]
                        except KeyError:
                            pass
                        try:
                            fld[WIDGET].required = form.optional_attrs[ANNUAL]['required'][fld[NAME]]
                        except KeyError:
                            pass
            except SubjectVisit.DoesNotExist:
                pass
        return form
