from datetime import datetime
from django.conf import settings
import logging
import pyodbc


class ExportDmis(object):

    def receive_on_dmis(self, request, requisition):
        dmis_identifier = None
        cnxn = pyodbc.connect(settings.DMIS_DATA_SOURCE)
        cursor = cnxn.cursor()
        # check if already received
        sql = ("select edc_specimen_identifier from lab01response "
               "where edc_specimen_identifier='{0}'").format(requisition.specimen_identifier)
        if not cursor.execute(str(sql)):
            if dmis_identifier:
                sql = self.get_dmis_insert_sql(requisition, request.user, dmis_identifier)
                cursor.execute(str(sql))
        return dmis_identifier, True

    def get_dmis_insert_sql(self, requisition, user, dmis_identifier):
        """ Prepares an sql staement to insert a new receiving record
        into the dmis receiving table based on data in the edc requisition."""

        return ("insert into lab01response ("
            "pid, pat_id, tid, headerdate,"
            "edc_specimen_identifier, sample_protocolnumber,"
            "sample_date_drawn, sample_time_drawn, sample_condition,"
            "sample_comment, sample_site_id, sample_visitid,"
            "pinitials, gender, dob, keyopcreated,"
            "keyoplastmodified, datecreated, datelastmodified) "
            "values("
            "'{pid}','{pat_id}','{tid}','{headerdate}','{edc_specimen_identifier}',"
            "'{sample_protocolnumber}','{sample_date_drawn}','{sample_time_drawn}',"
            "'{sample_condition}','{sample_comment}','{sample_site_id}','{sample_visitid}',"
            "'{pinitials}','{gender}','{dob}','{keyopcreated}',"
            "'{keyoplastmodified}','{datecreated}',"
            "'{datelastmodified}'").format(
                pid=dmis_identifier,
                pat_id=requisition.get_subject_identifier(),
                tid='000', headerdate=datetime.today().strftime('%Y-%m-%d %H:%M'),
                edc_specimen_identifier=requisition.specimen_identifier,
                sample_protocolnumber=settings.PROJECT_NUMBER,
                sample_date_drawn=requisition.requisition_datetime.strftime('%Y-%m-%d'),
                sample_time_drawn=requisition.requisition_datetime.strftime('%H:%M'),
                sample_condition='10',
                sample_comment='auto-import from edc',
                sample_site_id=requisition.site.site_code,
                sample_visitid=requisition.subject_visit.appointment.visit_definition.code,
                pinitials=requisition.subject_visit.appointment.registered_subject.initials,
                gender=requisition.subject_visit.appointment.registered_subject.gender,
                dob=requisition.subject_visit.appointment.registered_subject.dob.strftime('%Y-%m-%d'),
                keyopcreated=user,
                keyoplastmodified=user,
                datecreated=datetime.today().strftime('%Y-%m-%d %H:%M'),
                datelastmodified=datetime.today().strftime('%Y-%m-%d %H:%M'))
