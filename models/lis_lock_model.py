from bhp_lock.models import BaseLockModel


class LisLockModel(BaseLockModel):

    """ Track who is updating from django-lis to django-edc.

    The lock data is on the django-lis and managed by clients via :class:LisLock.

    ..seealso:: :class:`LisLock`."""

    class Meta:
        app_label = 'lab_import_lis'
