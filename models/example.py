#from django.db import models
#from django.db.models import Q
#from audit_trail.audit import AuditTrail
#from bhp_contact.models import BaseContactLogItem
#from base_model_with_infant_visit import BaseModelWithInfantVisit
#
#
#class InfantContactLog(BaseModelWithInfantVisit):
#
#    objects = models.Manager()
#
#    history = AuditTrail()
#
#    class Meta:
#        app_label = "maikalelo_infant"
#        verbose_name = "Infant Contact Log"
#        unique_together = (('infant_visit'),)
#
#
#class InfantContactLogItem(BaseContactLogItem):
#
#    infant_contact_log = models.ForeignKey(InfantContactLog)
#
#    objects = models.Manager()
#
#    history = AuditTrail()
#
#    class Meta:
#        app_label = "maikalelo_infant"
