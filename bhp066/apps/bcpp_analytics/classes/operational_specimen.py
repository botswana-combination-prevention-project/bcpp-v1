import collections
import datetime
from edc.constants import NO

from bhp066.apps.bcpp_lab.models import SubjectRequisition

from .base_operational_report import BaseOperationalReport


class OperationalSpecimen(BaseOperationalReport):

    def report_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        if self.survey.find('----') != -1:
            self.survey = ''
        self.date_to += datetime.timedelta(days=1)
        requisitions = SubjectRequisition.objects.filter(community__icontains=self.community,
                                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                                      user_modified__icontains=self.ra_username,
                                                      subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey)
        number_requisitions = requisitions.count()
        self.data_dict['1. Total No. of requisitions'] = number_requisitions
        requisitions_received = requisitions.filter(is_receive=True).count()
        self.data_dict['2. Total No. of requisitions received'] = requisitions_received
        microtube_requisitions = requisitions.filter(panel__name='Microtube').count()
        self.data_dict['3. Total No. of microtube requisitions'] = microtube_requisitions
        failed_microtube = requisitions.filter(panel__name='Microtube', is_drawn=NO).count()
        self.data_dict['4. Total No. of FAILED microtube requisitions'] = failed_microtube
        viral_load_requisitions = requisitions.filter(panel__name='Viral Load').count()
        self.data_dict['5. Total No. of viral load requisitions'] = viral_load_requisitions
        rbd_requisitions = requisitions.filter(panel__name='Research Blood Draw').count()
        self.data_dict['6. Total No. of research blood draw requisitions'] = rbd_requisitions
        venous_requisitions = requisitions.filter(panel__name='Venous (HIV)').count()
        self.data_dict['7. Total No. of venous requisitions requisitions'] = venous_requisitions
        elisa_requisitions = requisitions.filter(panel__name='ELISA').count()
        self.data_dict['8. Total No. of elisa requisitions requisitions'] = elisa_requisitions

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values