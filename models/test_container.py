from django.db import models
from audit_trail.audit import AuditTrail
from bhp_dispatch.models import BaseDispatchSyncUuidModel


class TestContainer(BaseDispatchSyncUuidModel):

    test_container_identifier = models.CharField(max_length=35, unique=True)

    comment = models.CharField(max_length=50, null=True)

    history = AuditTrail()

    def dispatched_as_container_identifier_attr(self, using=None):
        return 'test_container_identifier'

    def is_dispatch_container_model(self):
        return True

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'
