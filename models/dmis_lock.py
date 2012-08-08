from lab_import.models import BaseLockModel


class DmisLock(BaseLockModel):

    """ Track who is updating from dmis to django-lis.

    The lock data is on the django-lis and managed by clients via :class:DmisLock.

    ..seealso:: :class:DmisLock."""

    class Meta:
        app_label = 'lab_import_dmis'
