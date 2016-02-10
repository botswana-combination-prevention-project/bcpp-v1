# from datetime import timedelta
#
# from django.db.models import get_model
#
# from edc.subject.consent.managers import BaseConsentHistoryManager
#
#
# class ConsentHistoryManager(BaseConsentHistoryManager):
#
#     def get_by_natural_key(self, consent_datetime, survey_name, subject_identifier_as_pk):
#         margin = timedelta(minutes=5)
#         RegisteredSubject = get_model('registration', 'RegisteredSubject')
#         Survey = get_model('bcpp_survey', 'Survey')
#         survey = Survey.objects.get_by_natural_key(survey_name)
#         registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
#         return self.get(consent_datetime__range=(
# consent_datetime - margin, consent_datetime + margin), survey=survey, registered_subject=registered_subject)
#
#     def update_consent_history(self, consent_inst, created, using):
#         updated_values = {'consent_datetime': consent_inst.consent_datetime,
#                           'survey': consent_inst.survey,
#                           'household_member': consent_inst.household_member}
#         inst, created = super(ConsentHistoryManager, self).using(using).get_or_create(
#             registered_subject=consent_inst.registered_subject,
#             consent_app_label=consent_inst._meta.app_label,
#             consent_model_name=consent_inst._meta.object_name,
#             consent_pk=consent_inst.pk,
#             defaults=updated_values
#         )
#         if not created:
#             inst.consent_datetime = consent_inst.consent_datetime
#             inst.save(using=using)
