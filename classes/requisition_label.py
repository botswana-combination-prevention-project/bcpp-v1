from bhp_variables.models import StudySpecific
from bhp_registration.models import RegisteredSubject
from lab_barcode.classes import ModelLabel


class RequisitionLabel(ModelLabel):

    def prepare_label_context(self, **kwargs):
        """ A label subclass with the required key,value pairs expected by the label template.

        Receive the requisition instance, template and item count. Update kwargs
        with any key, values expected by the template """

        requisition = kwargs.get('instance')
        subject_identifier = requisition.get_subject_identifier()
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
        if registered_subject.may_store_samples.lower() == 'Yes':
            may_store_samples = 'Y'
        elif registered_subject.may_store_samples.lower() == 'No':
            may_store_samples = 'N'
        else:
            may_store_samples = '?'
        try:
            study_specific = StudySpecific.objects.all()[0]
        except:
            raise AttributeError('Cannot determine protocol_number. '
                                 'Please populate bhp_variables.study_specific.')
        custom = {}
        custom.update({
            'requisition_identifier': requisition.requisition_identifier,
            'barcode_value': requisition.barcode_value(),
            'specimen_identifier': requisition.specimen_identifier, })
        if 'hiv_status_code' in dir(requisition):
            custom.update({'hiv_status_code': str(requisition.hiv_status_code()), })
        if 'art_status_code' in dir(requisition):
            custom.update({'art_status_code': str(requisition.art_status_code()), })
        custom.update({
            'protocol': study_specific.protocol_number,
            'site': requisition.site.site_code,
            'panel': requisition.panel.name[0:21],
            'drawn_datetime': requisition.drawn_datetime,
            'subject_identifier': subject_identifier,
            'visit': requisition.get_visit().appointment.visit_definition.code,
            'gender': registered_subject.gender,
            'dob': registered_subject.dob,
            'initials': registered_subject.initials,
            'may_store_samples': may_store_samples,
            'aliquot_type': requisition.aliquot_type.alpha_code.upper(),
            'item_count_total': requisition.item_count_total, })
        self.label_context.update(**custom)
