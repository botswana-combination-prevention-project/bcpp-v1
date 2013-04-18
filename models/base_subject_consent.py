# # from django.db import models
# from bhp_botswana.models import BaseBwConsent
# from bhp_appointment_helper.models import BaseAppointmentMixin
# # from bhp_registration.models import RegisteredSubject
# 
# 
# class BaseSubjectConsent(BaseBwConsent, BaseAppointmentMixin):
#     
# #     registered_subject = models.ForeignKey(RegisteredSubject)
# 
#     """Model for subject consent and registration model for the subjects."""
#     
#     def __unicode__(self):
#         return self.subject_identifier
# 
#     def get_registration_datetime(self):
#         return self.consent_datetime
# 
#     def get_subject_type(self):
#         return 'subject'
# 
#     def get_subject_identifier(self):
#         return self.subject_identifier
# 
#     class Meta:
#         abstract = True
