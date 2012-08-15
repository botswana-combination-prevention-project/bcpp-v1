from django.db import models
from bhp_base_model.classes import BaseUuidModel
from lab_result.choices import RESULT_RELEASE_STATUS


class BaseResult(BaseUuidModel):

    result_identifier = models.CharField(
        max_length=25,
        editable=False,
        db_index=True)
    result_datetime = models.DateTimeField(
        help_text='Date result added to system.',
        db_index=True)
    release_status = models.CharField(
        max_length=25,
        choices=RESULT_RELEASE_STATUS,
        default='NEW',
        db_index=True)
    release_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date result authorized for release. This field will auto-fill if release status is changed',
        db_index=True)
    release_username = models.CharField(
        verbose_name="Release username",
        max_length=50,
        null=True,
        blank=True,
        help_text='Username of person authorizing result for release. This field will auto-fill if release status is changed',
        db_index=True)
    comment = models.CharField(
        verbose_name='Comment',
        max_length=50,
        null=True,
          blank=True,
        help_text='')
    dmis_result_guid = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        editable=False,
        help_text='dmis import value. N/A unless data imported from old system')
    receive_identifier = models.CharField(
        max_length=25, editable=False, null=True, db_index=True,
        help_text="non-user helper field to simplify search and filter")
    import_datetime = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.receive_identifier = self.order.aliquot.receive.receive_identifier
        super(BaseResult, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % (self.result_identifier)

    def panel(self):
        return unicode(self.order.panel)

    class Meta:
        abstract = True
