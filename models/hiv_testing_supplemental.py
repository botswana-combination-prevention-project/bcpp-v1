from django.db import models
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestingSupplemental (BaseScheduledVisitModel):
    
    """CS002"""
    
#     numhivtests = models.IntegerField(
#         verbose_name="Supplemental HT1. How many times before today have you had an HIV test?",
#         max_length=2,
#         null=True,
#         blank=True,
#         help_text="Note:Leave blank if participant does not want to respond.",
#         )
# 
#     wherehivtest = models.CharField(
#         verbose_name="Supplemental HT2. Where were you tested for HIV, the last [most recent] time you were tested?",
#         max_length=85,
#         null=True,
#         blank=True,
#         choices=WHEREHIVTEST_CHOICE,
#         help_text="",
#         )
# 
#     whyhivtest = models.CharField(
#         verbose_name="Supplemental HT3. Not including today's HIV test, which of the following statements best describes the reason you were tested the last [most recent] time you were tested before today?",
#         max_length=105,
#         null=True, 
#         blank=True,
#         choices=WHYHIVTEST_CHOICE,
#         help_text="",
#         )
# 
#     whynohivtest = models.CharField(
#         verbose_name="Supplemental HT4. If you were not tested for HIV in the 12 months prior to today, what is the main reason why not?",
#         max_length=55,
#         null=True, 
#         blank=True,
#         choices=WHYNOHIVTESTING_CHOICE,
#         help_text="",
#         )

    hiv_pills = models.CharField(
        verbose_name="Supplemental HT5. Have you ever heard about treatment for HIV with pills called antiretroviral therapy or ARVs [or HAART]?",
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    arvs_hiv_test = models.CharField(
        verbose_name="Supplemental HT6. Do you believe that treatment for HIV with antiretroviral therapy (or ARVs) can help HIV-positive people to live longer?",
        max_length=25,
        null=True, 
        blank=True,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        abstract = True
