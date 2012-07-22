from datetime import datetime
from django.db import models

try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.fields import InitialsField
from bhp_common.choices import YES_NO
from bhp_variables.models import StudySite, StudySpecific
from bhp_device.classes import Device
from bhp_string.classes import BaseString
from bhp_identifier.classes import CheckDigit
from lab_panel.models import Panel
from lab_aliquot_list.models import AliquotType
from lab_requisition.choices import PRIORITY, REASON_NOT_DRAWN, ITEM_TYPE
from lab_requisition.managers import BaseRequisitionManager
from lab_requisition.classes import RequisitionLabel


class BaseBaseRequisition (BaseUuidModel):

    """ does not include additional tests """

    requisition_identifier = models.CharField(
        verbose_name='Requisition Id',
        max_length=25,
        )

    requisition_datetime = models.DateTimeField(
        verbose_name='Requisition Date'
        )

    specimen_identifier = models.CharField(
        verbose_name='Specimen Id',
        max_length=25,
        null=True,
        blank=True,
        editable=False,
        unique=True,
        )

    protocol = models.CharField(
        verbose_name="Protocol Number",
        max_length=10,
        null=True,
        blank=True,
        help_text='Use three digit code e.g 041, 056, 062, etc'
        )

    site = models.ForeignKey(StudySite)

    clinician_initials = InitialsField(
        default='--',
        null=True,
        blank=True,
        )

    aliquot_type = models.ForeignKey(AliquotType,
        help_text='Note: Lists only those types associtaed with the Panel.')

    panel = models.ForeignKey(Panel)

    priority = models.CharField(
        verbose_name='Priority',
        max_length=25,
        choices=PRIORITY,
        default='normal',
        )

    is_drawn = models.CharField(
        verbose_name='Was a specimen drawn?',
        max_length=3,
        choices=YES_NO,
        default='Yes',
        help_text='If No, provide a reason below'
        )

    reason_not_drawn = models.CharField(
        verbose_name='If not drawn, please explain',
        max_length=25,
        choices=REASON_NOT_DRAWN,
        null=True,
        blank=True,
        )

    drawn_datetime = models.DateTimeField(
        verbose_name='Date / Time Specimen Drawn',
        null=True,
        blank=True,
        help_text='If not drawn, leave blank. Same as date and time of finger prick in case on DBS.',
        )

    item_type = models.CharField(
        verbose_name='Item collection type',
        max_length=25,
        choices=ITEM_TYPE,
        default='tube',
        help_text=''
        )

    item_count_total = models.IntegerField(
        verbose_name='Total number of items',
        default=1,
        help_text='Number of tubes, samples, cards, etc being sent for this test/order only. Determines number of labels to print',
        )

    estimated_volume = models.DecimalField(
        verbose_name='Estimated volume in mL',
        max_digits=7,
        decimal_places=1,
        default=5.0,
        help_text='If applicable, estimated volume of sample for this test/order. This is the total volume if number of "tubes" above is greater than 1'
        )

    comments = models.TextField(
        max_length=25,
        null=True,
        blank=True,
        )

    is_receive = models.BooleanField(
        verbose_name='received',
        default=False,
        )

    is_receive_datetime = models.DateTimeField(
        verbose_name='rcv-date',
        null=True,
        blank=True,
        )

    is_packed = models.BooleanField(
        verbose_name='packed',
        default=False,
        )

    is_labelled = models.BooleanField(
        verbose_name='labelled',
        default=False,
        )

    is_labelled_datetime = models.DateTimeField(
        verbose_name='label-date',
        null=True,
        blank=True,
        )

    is_lis = models.BooleanField(
        verbose_name='lis',
        default=False,
        )

    objects = BaseRequisitionManager()

    def __unicode__(self):
        return '%s' % (self.requisition_identifier)

    def get_infant_identifier(self):
        return self.get_visit().appointment.registered_subject.subject_identifier

    def subject(self):
        return self.get_subject_identifier()

    def visit(self):
        return self.get_visit().appointment.visit_definition.code

    def get_subject_identifier(self):
        return self.get_visit().appointment.registered_subject.subject_identifier

    def barcode_value(self):
        return self.specimen_identifier

    def label_template(self):
        raise TypeError('Override method label_template() on the requisition model '
                        'to return the correct template.')

    def save(self, *args, **kwargs):
        if not kwargs.get('suppress_autocreate_on_deserialize', False):
            if not self.requisition_identifier and self.is_drawn.lower() == 'yes':
                self.requisition_identifier = self.prepare_requisition_identifier()
            if self.requisition_identifier and not self.specimen_identifier:
                self.specimen_identifier = self.prepare_specimen_identifier()

        return super(BaseBaseRequisition, self).save(*args, **kwargs)

    def prepare_specimen_identifier(self, **kwargs):
        """ add protocol, site and check digit"""
        check_digit = CheckDigit()
        study_specific = StudySpecific.objects.get_query_set()[0]
        #check_digit = CheckDigit()
        self.protocol = study_specific.protocol_code
        opts = {}
        opts.update({'protocol': study_specific.protocol_prefix})
        opts.update({'requisition_identifier': self.requisition_identifier, 'site': self.site})
        opts.update({'check_digit': check_digit.calculate('{protocol}{site}{requisition_identifier}'.format(opts),
                                                           modulus=7)})
        return '{protocol}-{site}{requisition_identifier}-{check-digit}'.format(opts)

    def prepare_requisition_identifier(self, **kwargs):
        """Generate and return a locally unique requisition identifier for a device (adds device id)"""
        device = Device()
        string = BaseString()
        length = 5
        template = '{device_id}{random_string}'
        opts = {'device_id': device.device_id, 'random_string': string.get_safe_random_string(length=length)}
        requisition_identifier = template.format(**opts)
        # look for a duplicate
        if self.__class__.objects.filter(requisition_identifier=requisition_identifier):
            n = 1
            while self.__class__.objects.filter(requisition_identifier=requisition_identifier):
                requisition_identifier = template.format(**opts)
                n += 1
                if n == length ** len(string.safe_allowed_chars):
                    raise TypeError('Unable prepare a unique requisition identifier, '
                                    'all are taken. Increase the length of the random string')
        return requisition_identifier

    def print_label(self, request, **kwargs):
        """ print a label using the label class or subclass returned by get_label()"""
        if self.specimen_identifier:
            requisition_label = RequisitionLabel()
            requisition_label.print_label(request, self, self.item_count_total,
                                          self.specimen_identifier)
            self.is_labelled = True
            self.modified = datetime.today()
            self.save()

    class Meta:
        abstract = True
