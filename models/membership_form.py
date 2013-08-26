from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.urlresolvers import reverse
from bhp_content_type_map.models import ContentTypeMap
from bhp_base_model.models import BaseUuidModel
from bhp_visit.managers import MembershipFormManager
from bhp_appointment_helper.models import BaseAppointmentMixin


class MembershipForm(BaseUuidModel):

    """Model to list forms to be linked to a ShceduleGroup as "registration" forms to that group"""

    content_type_map = models.OneToOneField(
        ContentTypeMap,
        related_name='+'
        )

    category = models.CharField(
        max_length=25,
        default='subject',
        null=True,
        help_text='In lowercase, this should be a valid subject type (as in registered_subject).'
        )

    visible = models.BooleanField(
        default=True,
        help_text='If not visible on the dashboard, you have to write code to populate it yourself.'
        )

    objects = MembershipFormManager()

    def save(self, *args, **kwargs):
        # get the model class
        cls = self.content_type_map.model_class()
        # inspect for registered subject attribute
        if not 'registered_subject' in dir(cls):
            raise ValidationError('Membership forms must have a key to model RegisteredSubject. Got {0}'.format(cls))
        if not issubclass(cls, BaseAppointmentMixin):
            raise ImproperlyConfigured('MembershipForm attribute content_type_map must refer to a model class that is a subclass of BaseAppointmentMixin. Got {0}'.format(cls))
        super(MembershipForm, self).save(*args, **kwargs)

    def natural_key(self):
        return self.content_type_map.natural_key()

    def get_absolute_url(self):
        return reverse('admin:bhp_visit_membershipform_change', args=(self.id,))

    def __unicode__(self):
        return self.content_type_map.name

    class Meta:
        app_label = "bhp_visit"
