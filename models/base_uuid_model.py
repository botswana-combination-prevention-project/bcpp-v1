from bhp_dispatch.models import BaseDispatchSyncUuidModel


class BaseUuidModel(BaseDispatchSyncUuidModel):

    class Meta:
        abstract = True
