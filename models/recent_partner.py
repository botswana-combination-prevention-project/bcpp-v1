from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from detailed_sexual_history import DetailedSexualHistory


class RecentPartner (DetailedSexualHistory):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_recentpartner_change', args=(self.id,))
    
#     def get_result_value(self, attr=None):
#         """Returns a result value for given attr name for the lab_tracker."""
#         retval = None
#         if not attr in dir(self):
#             raise TypeError('Attribute {0} does not exist in model {1}'.format(attr, self._meta.object_name))
#         if attr == 'partner_status':
#             if self.partner_status.lower() == 'pos':
#                 retval = 'POS'
#             elif self.partner_status.lower() == 'neg':
#                 retval = 'NEG'
#             else:
#                 retval = 'UNKNOWN'
#         return retval


    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Most Recent Partner"
        verbose_name_plural = "CS003: Most Recent Partner"
