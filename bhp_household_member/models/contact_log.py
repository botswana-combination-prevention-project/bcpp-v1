# from django.db import models
# from django.core.urlresolvers import reverse
# from bhp_common.choices import YES_NO
# from bcpp_household.choices import INFO_PROVIDER, STATUS
# from base_uuid_model import BaseUuidModel
# 
# 
# class ContactLog(BaseUuidModel):
# 
#     def get_absolute_url(self):
#         return reverse('admin:bcpp_household_contactlog_change', args=(self.id, ))
# 
#     class Meta:
#         app_label = 'bcpp_household'
# 
# 
# class ContactLogItem(BaseUuidModel):
# 
#     contact_log = models.ForeignKey(ContactLog)
# 
#     contact_datetime = models.DateTimeField()
# 
#     subject_status = models.CharField(
#         verbose_name='Subject Status',
#         max_length=10,
#         choices=STATUS)
# 
#     is_contacted = models.CharField(
#         verbose_name='Contacted?',
#         max_length=10,
#         choices=YES_NO)
# 
#     information_provider = models.CharField(
#         choices=INFO_PROVIDER,
#         max_length=20,
#         help_text="",
#         null=True,
#         blank=True,
#         )
# 
#     appointment_datetime = models.DateTimeField(
#         verbose_name='Appointment',
#         null=True, blank=True)
# 
#     try_again = models.CharField(
#         verbose_name="Try to contact again?",
#         max_length=10,
#         choices=YES_NO)
# 
#     comment = models.TextField(
#         max_length=50,
#         blank=True,
#         null=True,
#         )
# 
#     class Meta:
#         app_label = 'bcpp_household'
