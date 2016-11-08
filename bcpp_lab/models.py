from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_lab.requisition.model_mixins import RequisitionModelMixin
from edc_metadata.model_mixins import UpdatesRequisitionMetadataModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from bcpp_subject.models.subject_visit import SubjectVisit
from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models.url_mixin import UrlMixin


class SubjectRequisition(SyncModelMixin, CrfModelMixin, RequisitionModelMixin, RequiresConsentMixin,
                         UpdatesRequisitionMetadataModelMixin, UrlMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_lab_admin'

    subject_visit = models.ForeignKey(SubjectVisit)

    class Meta:
        app_label = 'bcpp_lab'
        consent_model = 'bcpp_subject.subjectconsent'
