from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO
from base_scheduled_visit_model import BaseScheduledVisitModel


class ReproductiveHealth (BaseScheduledVisitModel):
    
    """CS002"""
    
    number_children = models.IntegerField(
        verbose_name=("How many children have you given birth to? Please include any"
                      " children that may have died at (stillbirth) or after birth. "
                      "Do not include any current pregnancies or miscarriages that occur"
                      " early in pregnancy (prior to 20 weeks)."),
        max_length=2,
        default=0,
        help_text=("Note: If participant does not want to answer, please record 0. "
                   "If no children, skip questions 84-87."),
        )
    
    menopause = models.CharField(
        verbose_name="Have you reached menopause (more than 12 months without a period)?",
        max_length=3,
        choices=YES_NO,
        help_text="this also refers to pre-menopause",
        )
    
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_reproductivehealth_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Reproductive Health"
        verbose_name_plural = "Reproductive Health"
