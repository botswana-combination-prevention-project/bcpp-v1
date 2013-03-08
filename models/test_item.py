from django.db import models
from audit_trail.audit import AuditTrail
from base_dispatch_sync_uuid_model import BaseDispatchSyncUuidModel
from test_container import TestContainer


class TestItem(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestContainer)

    comment = models.CharField(max_length=50, null=True)

    history = AuditTrail()

#    def dispatched_as_container_identifier_attr(self):
#        return 'test_item_identifier'

    def is_dispatch_container_model(self):
        return False

    def dispatch_item_container_reference(self, using=None):
        return (TestContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'
